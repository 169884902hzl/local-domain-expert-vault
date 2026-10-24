const { ItemView, Modal, Notice, Plugin, PluginSettingTab, Setting, TFile } = require("obsidian");
const childProcess = require("child_process");
const path = require("path");

const VIEW_TYPE_PAPER_SOURCE = "paper-reading-workbench-source";
const VIEW_TYPE_PAPER_CONTROL = "paper-reading-workbench-control";
const DEFAULT_SETTINGS = {
  translationMaxConcurrency: 5,
  translationTimeoutSec: 1200,
  translationModel: "gemini-3.1-pro-preview",
  pythonCommand: "python",
  openControlPanelOnStartup: false,
};

const MAX_TRANSLATION_CONCURRENCY = 5;
const ZOTERO_FETCH_TIMEOUT_MS = 1500;

module.exports = class PaperReadingWorkbenchPlugin extends Plugin {
  async onload() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    this.settings.translationMaxConcurrency = clampConcurrency(this.settings.translationMaxConcurrency);
    await this.saveData(this.settings);
    this.registerView(VIEW_TYPE_PAPER_SOURCE, (leaf) => new PaperSourceView(leaf, this));
    this.registerView(VIEW_TYPE_PAPER_CONTROL, (leaf) => new PaperWorkbenchControlView(leaf, this));
    this.addRibbonIcon("microscope", "Paper Workbench", async () => {
      await this.openWorkbenchFromCurrentOrPanel();
    });
    const statusBar = this.addStatusBarItem();
    statusBar.addClass("paper-workbench-statusbar-button");
    statusBar.setText("Paper Workbench");
    statusBar.addEventListener("click", async () => {
      await this.openWorkbenchFromCurrentOrPanel();
    });
    if (this.settings.openControlPanelOnStartup) {
      this.app.workspace.onLayoutReady(async () => {
        await this.openControlPanel();
      });
    }

    this.addCommand({
      id: "open-current-paper-workbench",
      name: "Open paper reading workbench for current note",
      callback: async () => {
        const key = await this.resolveCurrentZoteroKey();
        if (!key) {
          new Notice("No zotero_key found in the active note.");
          return;
        }
        await this.openWorkbenchForKey(key);
      },
    });

    this.addCommand({
      id: "open-paper-workbench-by-zotero-key",
      name: "Open paper reading workbench by Zotero key",
      callback: () => {
        new ZoteroKeyModal(this.app, async (key) => {
          await this.openWorkbenchForKey(key);
        }).open();
      },
    });

    this.addCommand({
      id: "translate-current-paper-cache",
      name: "Generate translation cache for current paper",
      callback: async () => {
        const key = await this.resolveCurrentZoteroKey();
        if (!key) {
          new Notice("No zotero_key found in the active note.");
          return;
        }
        await this.runTranslation([key]);
      },
    });

    this.addCommand({
      id: "generate-current-paper-knowledge-diagram",
      name: "Generate deep knowledge diagram for current paper",
      callback: async () => {
        const key = await this.resolveCurrentZoteroKey();
        if (!key) {
          new Notice("No zotero_key found in the active note.");
          return;
        }
        await this.openOrGenerateKnowledgeDiagram(key);
      },
    });

    this.addCommand({
      id: "open-paper-workbench-control-panel",
      name: "Open paper workbench control panel",
      callback: async () => {
        await this.openControlPanel();
      },
    });

    this.addSettingTab(new PaperReadingWorkbenchSettingTab(this.app, this));
  }

  async openControlPanel() {
    const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE_PAPER_CONTROL)[0];
    if (existing) {
      this.app.workspace.revealLeaf(existing);
      return;
    }
    const leaf = this.app.workspace.getLeaf("tab");
    await leaf.setViewState({ type: VIEW_TYPE_PAPER_CONTROL, active: true });
    this.app.workspace.revealLeaf(leaf);
  }

  async openWorkbenchFromCurrentOrPanel() {
    const key = await this.resolveCurrentZoteroKey();
    if (key) {
      await this.openWorkbenchForKey(key);
      return;
    }
    new Notice("No zotero_key found in the active note; opening Paper Workbench control panel.");
    await this.openControlPanel();
  }

  async resolveCurrentZoteroKey() {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) return "";
    const cache = this.app.metadataCache.getFileCache(activeFile);
    const frontmatterKey = cache && cache.frontmatter && cache.frontmatter.zotero_key;
    if (frontmatterKey) return String(frontmatterKey).replace(/^"|"$/g, "").trim().toUpperCase();
    const text = await this.app.vault.read(activeFile);
    const match = text.match(/^zotero_key:\s*"?([A-Z0-9]+)"?\s*$/m);
    return match ? match[1].toUpperCase() : "";
  }

  async openWorkbenchForKey(rawKey) {
    const key = String(rawKey || "").trim().toUpperCase();
    if (!key) return;
    new Notice(`Preparing paper workbench for ${key}...`);
    const paper = await this.resolvePaperContext(key);
    if (!paper.topicFile) {
      new Notice(`No topic note found for Zotero key ${key}.`);
      return;
    }
    await this.ensureWorkbenchArtifacts(paper);
    await this.openFourPaneLayout(paper);
    new Notice(`Opened reading workbench for ${key}.`);
  }

  async resolvePaperContext(key) {
    const topicFile = await this.findTopicByZoteroKey(key);
    const topicText = topicFile ? await this.app.vault.read(topicFile) : "";
    const title = readFrontmatterField(topicText, "title") || (topicFile ? topicFile.basename : key);
    const slug = topicFile ? topicFile.basename : key.toLowerCase();
    const rawReadingPath = `raw/readings/${key}-analysis.md`;
    const rawReadingFile = this.app.vault.getAbstractFileByPath(rawReadingPath);
    const zotero = await this.resolveZoteroSource(key);
    const arxiv = await this.findArxivMetadata(key, title);
    const entryPath = `projects/reading-workbench/${key}-zotero-source.md`;
    const ideaPath = `projects/reading-workbench/${key}-gemini-ideas.md`;
    const translationPath = `projects/translations/${key}-zh.md`;
    const diagramPath = `projects/knowledge-diagrams/papers/${slug}.md`;
    return {
      key,
      title,
      slug,
      topicFile,
      rawReadingFile: rawReadingFile instanceof TFile ? rawReadingFile : null,
      zotero,
      arxiv,
      entryPath,
      ideaPath,
      translationPath,
      diagramPath,
    };
  }

  async findTopicByZoteroKey(key) {
    const files = this.app.vault.getMarkdownFiles().filter((file) => file.path.startsWith("wiki/topics/"));
    for (const file of files) {
      const cache = this.app.metadataCache.getFileCache(file);
      const frontmatterKey = cache && cache.frontmatter && cache.frontmatter.zotero_key;
      if (frontmatterKey && String(frontmatterKey).replace(/^"|"$/g, "").toUpperCase() === key) {
        return file;
      }
    }
    for (const file of files) {
      const text = await this.app.vault.cachedRead(file);
      const match = text.match(/^zotero_key:\s*"?([A-Z0-9]+)"?\s*$/m);
      if (match && match[1].toUpperCase() === key) return file;
    }
    return null;
  }

  async resolveZoteroSource(key) {
    const fallback = {
      status: "unavailable",
      error: "",
      itemUri: `zotero://select/library/items/${key}`,
      itemUrl: "",
      bestAttachmentUri: "",
      bestAttachmentPath: "",
      attachments: [],
    };
    try {
      const itemResponse = await fetchWithTimeout(`http://localhost:23119/api/users/0/items/${encodeURIComponent(key)}?format=json`, ZOTERO_FETCH_TIMEOUT_MS);
      if (!itemResponse.ok) throw new Error(`item_http_${itemResponse.status}`);
      const item = await itemResponse.json();
      const childResponse = await fetchWithTimeout(`http://localhost:23119/api/users/0/items/${encodeURIComponent(key)}/children?format=json`, ZOTERO_FETCH_TIMEOUT_MS);
      const children = childResponse.ok ? await childResponse.json() : [];
      const attachments = Array.isArray(children)
        ? children
            .filter((child) => child && child.data && child.data.itemType === "attachment")
            .map((child) => {
              const data = child.data || {};
              const attachmentKey = child.key || data.key || "";
              const isPdfAttachment = /pdf/i.test(data.contentType || "") || /\.pdf$/i.test(data.path || data.localPath || data.filename || "") || /\/pdf\//i.test(data.url || "");
              return {
                key: attachmentKey,
                title: data.title || data.filename || "attachment",
                contentType: data.contentType || "",
                linkMode: data.linkMode || "",
                path: data.path || data.localPath || data.filename || "",
                url: data.url || "",
                uri: attachmentKey ? (isPdfAttachment ? `zotero://open-pdf/library/items/${attachmentKey}` : `zotero://select/library/items/${attachmentKey}`) : "",
              };
            })
        : [];
      const best = attachments.find((attachment) => /pdf/i.test(attachment.contentType) || /\.pdf$/i.test(attachment.path) || /\/pdf\//i.test(attachment.url)) || attachments[0] || {};
      return {
        status: "ok",
        error: "",
        itemUri: `zotero://select/library/items/${key}`,
        itemUrl: item && item.data ? item.data.url || "" : "",
        bestAttachmentUri: best.uri || "",
        bestAttachmentPath: best.path || "",
        attachments,
      };
    } catch (error) {
      return Object.assign({}, fallback, { error: `zotero_local_api_unavailable:${error.message}` });
    }
  }

  async findArxivMetadata(key, title) {
    const result = {
      arxivId: "",
      url: "",
      pdfUrl: "",
      source: "",
    };
    const dailyFiles = this.app.vault.getFiles().filter((file) => {
      return file.path.startsWith("projects/arxiv-daily/") && file.path.endsWith("-candidates.jsonl");
    }).sort((a, b) => b.path.localeCompare(a.path));
    for (const file of dailyFiles.slice(0, 30)) {
      const text = await this.app.vault.cachedRead(file);
      if (!text.includes(key)) continue;
      for (const line of text.split(/\r?\n/)) {
        if (!line.includes(key)) continue;
        try {
          const row = JSON.parse(line);
          const paper = row.paper || {};
          result.arxivId = String(paper.arxiv_id || "");
          result.url = String(paper.url || "");
          result.pdfUrl = String(paper.pdf_url || "");
          result.source = file.path;
          return result;
        } catch (error) {
          continue;
        }
      }
    }
    const runFiles = this.app.vault.getFiles().filter((file) => {
      return file.path.startsWith("projects/arxiv-daily/") && file.path.endsWith("-run.md");
    }).sort((a, b) => b.path.localeCompare(a.path));
    for (const file of runFiles.slice(0, 30)) {
      const text = await this.app.vault.cachedRead(file);
      const line = text.split(/\r?\n/).find((item) => item.includes(`zotero_key=${key}`));
      if (!line) continue;
      const match = line.match(/arxiv=([0-9.]+)/);
      if (match) {
        result.arxivId = match[1];
        result.url = `https://arxiv.org/abs/${match[1]}`;
        result.pdfUrl = `https://arxiv.org/pdf/${match[1]}`;
        result.source = file.path;
        return result;
      }
    }
    if (title) result.source = "topic_note_only";
    return result;
  }

  async ensureWorkbenchArtifacts(paper) {
    await this.ensureFolder("projects/reading-workbench");
    await this.ensureFolder("projects/translations");
    await this.ensureFolder("projects/knowledge-diagrams");
    await this.ensureFolder("projects/knowledge-diagrams/papers");
    await this.writeIfChanged(paper.entryPath, this.renderZoteroSourceEntry(paper));
    const ideaFile = this.app.vault.getAbstractFileByPath(paper.ideaPath);
    if (!(ideaFile instanceof TFile) || await this.shouldRefreshGeneratedIdeaFile(ideaFile)) {
      await this.writeIfChanged(paper.ideaPath, await this.renderIdeaPage(paper));
    }
    const translationFile = this.app.vault.getAbstractFileByPath(paper.translationPath);
    if (!(translationFile instanceof TFile)) {
      await this.app.vault.create(paper.translationPath, this.renderTranslationPlaceholder(paper));
    }
  }

  async ensureFolder(folderPath) {
    if (!this.app.vault.getAbstractFileByPath(folderPath)) {
      await this.app.vault.createFolder(folderPath);
    }
  }

  async writeIfChanged(filePath, content) {
    const existing = this.app.vault.getAbstractFileByPath(filePath);
    if (existing instanceof TFile) {
      const oldContent = await this.app.vault.read(existing);
      if (oldContent !== content) await this.app.vault.modify(existing, content);
      return;
    }
    await this.app.vault.create(filePath, content);
  }

  async shouldRefreshGeneratedIdeaFile(file) {
    if (!(file instanceof TFile)) return false;
    const content = await this.app.vault.read(file);
    if (content.includes('idea_page_schema: "bilingual-v1"')) return false;
    if (content.includes("## Manual Notes") || content.includes("## 人工")) return false;
    return content.includes("tags: [paper-workbench, gemini, idea]") && content.includes("## Matched Candidates");
  }

  renderZoteroSourceEntry(paper) {
    const arxivLine = paper.arxiv.url ? `- arXiv: ${paper.arxiv.url}` : "- arXiv: not found in local daily records";
    const pdfLine = paper.arxiv.pdfUrl ? `- PDF URL: ${paper.arxiv.pdfUrl}` : "- PDF URL: not found in local daily records";
    const zotero = paper.zotero || {};
    const attachmentLines = zotero.attachments && zotero.attachments.length
      ? zotero.attachments.slice(0, 8).map((item) => {
          const uri = item.uri ? `[${item.title || item.key}](${item.uri})` : (item.title || item.key || "attachment");
          const pathLine = item.path ? `\n  - path: \`${item.path}\`` : "";
          const urlLine = item.url ? `\n  - url: ${item.url}` : "";
          const storage = item.path ? "file-backed" : (item.url ? "pdf-url" : item.linkMode || "-");
          return `- Attachment: ${uri} — ${item.contentType || item.linkMode || "-"}; storage: ${storage}${pathLine}${urlLine}`;
        }).join("\n")
      : "- Attachments: not resolved from Zotero local API";
    return `---\ntitle: "Zotero Source - ${escapeYaml(paper.title)}"\ntags: [paper-workbench, zotero-source]\ncreated: "${todayIso()}"\nupdated: "${todayIso()}"\ntype: "permanent"\nstatus: "stub"\nsummary: "Zotero-first source entry for paper reading workbench."\nzotero_key: "${paper.key}"\nzotero_source_status: "${zotero.status || "unavailable"}"\n---\n# Zotero Source - ${paper.title}\n\n- Zotero item: [${paper.key}](${zotero.itemUri || `zotero://select/library/items/${paper.key}`})\n- Zotero local status: \`${zotero.status || "unavailable"}\`\n${zotero.error ? `- Zotero warning: \`${zotero.error}\`\n` : ""}${attachmentLines}\n${arxivLine}\n${pdfLine}\n- Topic note: [[${paper.topicFile.path}]]\n${paper.rawReadingFile ? `- Deep reading: [[${paper.rawReadingFile.path}]]` : "- Deep reading: not found"}\n- Gemini ideas: [[${paper.ideaPath}]]\n- Translation cache: [[${paper.translationPath}]]\n- Knowledge diagram: [[${paper.diagramPath}]]\n\n> Boundary: Zotero remains the source of truth for the original PDF. This note stores source links and local reading context; it does not copy PDFs into the vault.\n`;
  }

  async renderIdeaPage(paper) {
    const matches = await this.findGeminiIdeaMatches(paper);
    const lines = [
      "---",
      `title: "Gemini Ideas - ${escapeYaml(paper.title)}"`,
      "tags: [paper-workbench, gemini, idea]",
      `created: "${todayIso()}"`,
      `updated: "${todayIso()}"`,
      'type: "permanent"',
      'status: "stub"',
      'summary: "Filtered Gemini greenhouse candidates related to this paper."',
      'idea_page_schema: "bilingual-v1"',
      `zotero_key: "${paper.key}"`,
      "---",
      `# Gemini Ideas - ${paper.title}`,
      "",
      `- Topic note: [[${paper.topicFile.path}]]`,
      paper.rawReadingFile ? `- Deep reading: [[${paper.rawReadingFile.path}]]` : "- Deep reading: not found",
      "",
      "## Matched Candidates",
      "",
    ];
    if (!matches.length) {
      lines.push("- No direct candidate match found in recent greenhouse archives.");
      lines.push("- Use this pane as the manual idea review slot for this paper.");
    } else {
      for (const item of matches.slice(0, 8)) {
        lines.push(`### ${item.title || "Untitled candidate"}`);
        lines.push(`- archive: \`${item.archive}\``);
        lines.push(`- tier: ${item.quality_tier || "-"}; label: ${item.greenhouse_label || "-"}; group: ${item.candidate_group || "-"}`);
        lines.push("");
        lines.push("#### 中文导读");
        lines.push(...renderCandidateChineseBrief(item));
        lines.push("");
        lines.push("#### Original Fields");
        if (item.problem) lines.push(`- problem: ${item.problem}`);
        if (item.mechanism) lines.push(`- mechanism: ${item.mechanism}`);
        if (item.strongest_baseline) lines.push(`- strongest_baseline: ${item.strongest_baseline}`);
        if (item.killer_experiment) lines.push(`- killer_experiment: ${item.killer_experiment}`);
        lines.push("");
      }
    }
    return lines.join("\n") + "\n";
  }

  async findGeminiIdeaMatches(paper) {
    const archives = this.app.vault.getFiles().filter((file) => {
      return file.path.startsWith("projects/research-agenda/divergent/") && file.path.endsWith("-gemini-raw-candidates.json");
    }).sort((a, b) => b.path.localeCompare(a.path));
    const titleTokens = normalizeWords(paper.title).filter((token) => token.length >= 7).slice(0, 8);
    const strongNeedles = [paper.key.toLowerCase(), paper.slug.toLowerCase()];
    const matches = [];
    for (const file of archives.slice(0, 20)) {
      let data;
      try {
        data = JSON.parse(await this.app.vault.cachedRead(file));
      } catch (error) {
        continue;
      }
      const candidates = data.raw_gemini_candidates || [];
      for (const candidate of candidates) {
        const text = JSON.stringify(candidate).toLowerCase();
        const directScore = strongNeedles.reduce((acc, needle) => acc + (needle && text.includes(needle) ? 5 : 0), 0);
        const tokenScore = titleTokens.reduce((acc, needle) => acc + (needle && text.includes(needle) ? 1 : 0), 0);
        const score = directScore + tokenScore;
        if (directScore > 0 || tokenScore >= 3) matches.push(Object.assign({ archive: file.path, match_score: score }, candidate));
      }
    }
    return matches.sort((a, b) => (b.match_score || 0) - (a.match_score || 0)).slice(0, 6);
  }

  renderTranslationPlaceholder(paper) {
    return `---\ntitle: "AI Translation - ${escapeYaml(paper.title)}"\ntags: [paper-workbench, translation]\ncreated: "${todayIso()}"\nupdated: "${todayIso()}"\ntype: "permanent"\nstatus: "stub"\nsummary: "AI translation cache for paper reading workbench."\nzotero_key: "${paper.key}"\ntranslation_status: "not_generated"\ntranslation_source_scope: "pending"\ntranslation_concurrency_limit: ${MAX_TRANSLATION_CONCURRENCY}\n---\n# AI Translation - ${paper.title}\n\nTranslation cache has not been generated yet.\n\nUse command: **Paper Reading Workbench: Generate translation cache for current paper**.\n\nConcurrency policy: translation jobs are capped at ${MAX_TRANSLATION_CONCURRENCY} parallel Gemini calls.\n`;
  }

  async openFourPaneLayout(paper) {
    const readingFile = paper.topicFile;
    const ideaFile = this.app.vault.getAbstractFileByPath(paper.ideaPath);
    const translationFile = this.app.vault.getAbstractFileByPath(paper.translationPath);
    const sourceState = {
      type: VIEW_TYPE_PAPER_SOURCE,
      active: false,
      state: {
        key: paper.key,
        title: paper.title,
        entryPath: paper.entryPath,
        topicPath: paper.topicFile.path,
        arxivUrl: paper.arxiv.url,
        pdfUrl: paper.arxiv.pdfUrl,
        metadataSource: paper.arxiv.source,
        zotero: paper.zotero,
        diagramPath: paper.diagramPath,
      },
    };

    const centerLeaf = this.findOpenFileLeaf(readingFile) || this.app.workspace.getLeaf("tab");
    if (!this.findOpenFileLeaf(readingFile)) {
      await centerLeaf.openFile(readingFile, { active: true });
    }
    this.app.workspace.setActiveLeaf(centerLeaf, { focus: true });

    if (typeof centerLeaf.split === "function") {
      const leftLeaf = centerLeaf.split("vertical", true);
      await leftLeaf.setViewState(sourceState);

      const rightTopLeaf = centerLeaf.split("vertical", false);
      if (ideaFile instanceof TFile) await rightTopLeaf.openFile(ideaFile, { active: false });

      const rightBottomLeaf = rightTopLeaf.split("horizontal", false);
      if (translationFile instanceof TFile) await rightBottomLeaf.openFile(translationFile, { active: false });

      this.app.workspace.setActiveLeaf(centerLeaf, { focus: true });
      return;
    }

    const leftLeaf = this.app.workspace.getLeaf("split", "vertical");
    await leftLeaf.setViewState(sourceState);

    const rightTopLeaf = this.app.workspace.getLeaf("split", "vertical");
    if (ideaFile instanceof TFile) await rightTopLeaf.openFile(ideaFile, { active: false });

    const rightBottomLeaf = this.app.workspace.getLeaf("split", "horizontal");
    if (translationFile instanceof TFile) await rightBottomLeaf.openFile(translationFile, { active: false });

    this.app.workspace.setActiveLeaf(centerLeaf, { focus: true });
  }

  findOpenFileLeaf(file) {
    if (!(file instanceof TFile)) return null;
    const leaves = this.app.workspace.getLeavesOfType("markdown");
    return leaves.find((leaf) => {
      const viewFile = leaf.view && leaf.view.file;
      return viewFile instanceof TFile && viewFile.path === file.path;
    }) || null;
  }

  async runTranslation(keys) {
    const vaultBase = this.app.vault.adapter.basePath;
    const scriptPath = path.join(vaultBase, ".claude", "scripts", "translate_paper_workbench.py");
    const args = [
      scriptPath,
      "--zotero-keys",
      keys.join(","),
      "--max-concurrency",
      String(clampConcurrency(this.settings.translationMaxConcurrency)),
      "--timeout",
      String(this.settings.translationTimeoutSec || 1200),
      "--model",
      String(this.settings.translationModel || "gemini-3.1-pro-preview"),
    ];
    new Notice(`Starting translation cache for ${keys.join(", ")}; concurrency <= ${MAX_TRANSLATION_CONCURRENCY}.`);
    const proc = childProcess.spawn(this.settings.pythonCommand || "python", args, {
      cwd: vaultBase,
      shell: false,
      windowsHide: true,
    });
    let stderr = "";
    proc.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    proc.on("error", (error) => {
      new Notice(`Translation failed to start: ${error.message}`);
    });
    proc.on("close", (code) => {
      if (code === 0) {
        new Notice(`Translation cache finished for ${keys.join(", ")}.`);
      } else {
        new Notice(`Translation cache exited ${code}: ${stderr.slice(0, 160)}`);
      }
    });
  }

  async openZoteroItemForKey(key) {
    window.open(`zotero://select/library/items/${key}`);
  }

  async openZoteroPdfForSource(state) {
    const zotero = (state && state.zotero) || {};
    if (zotero.bestAttachmentUri) {
      window.open(zotero.bestAttachmentUri);
      return;
    }
    new Notice("This Zotero item has no PDF attachment yet. Opening the Zotero item instead.");
    if (zotero.itemUri || state.key) {
      window.open(zotero.itemUri || `zotero://select/library/items/${state.key}`);
    }
  }

  async openOrGenerateKnowledgeDiagram(key, diagramPath = "") {
    const normalizedKey = String(key || "").trim().toUpperCase();
    const resolvedPath = diagramPath || await this.resolveDiagramPathForKey(normalizedKey);
    if (await this.openDiagramFile(resolvedPath)) {
      new Notice(`Opened knowledge diagram for ${normalizedKey}.`);
      return;
    }
    await this.runKnowledgeDiagram(normalizedKey, resolvedPath);
  }

  async resolveDiagramPathForKey(key) {
    const paper = await this.resolvePaperContext(key);
    return paper.diagramPath;
  }

  async openDiagramFile(diagramPath) {
    if (!diagramPath) return false;
    const file = this.app.vault.getAbstractFileByPath(diagramPath);
    if (!(file instanceof TFile)) return false;
    const leaf = this.app.workspace.getLeaf("tab");
    await leaf.openFile(file, { active: true });
    this.app.workspace.revealLeaf(leaf);
    return true;
  }

  async runKnowledgeDiagram(key, diagramPath = "") {
    const vaultBase = this.app.vault.adapter.basePath;
    const scriptPath = path.join(vaultBase, ".claude", "scripts", "generate_knowledge_diagrams.py");
    const args = [scriptPath, "paper", "--zotero-key", key, "--depth", "deep"];
    new Notice(`Generating deep knowledge diagram for ${key}.`);
    const proc = childProcess.spawn(this.settings.pythonCommand || "python", args, {
      cwd: vaultBase,
      shell: false,
      windowsHide: true,
    });
    let stderr = "";
    proc.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    proc.on("error", (error) => {
      new Notice(`Knowledge diagram failed to start: ${error.message}`);
    });
    proc.on("close", (code) => {
      if (code === 0) {
        new Notice(`Knowledge diagram finished for ${key}; opening diagram.`);
        this.openDiagramFile(diagramPath).then((opened) => {
          if (!opened) new Notice(`Knowledge diagram finished, but file was not found yet: ${diagramPath || "unknown path"}`);
        });
      } else {
        new Notice(`Knowledge diagram exited ${code}: ${stderr.slice(0, 160)}`);
      }
    });
  }
};

class PaperSourceView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.viewState = {};
  }

  getViewType() {
    return VIEW_TYPE_PAPER_SOURCE;
  }

  getDisplayText() {
    return this.viewState.title ? `Zotero Source - ${this.viewState.title}` : "Zotero Source";
  }

  getIcon() {
    return "file-text";
  }

  async setState(state, result) {
    await super.setState(state, result);
    this.viewState = state || {};
    this.render();
  }

  async onOpen() {
    this.render();
  }

  render() {
    const container = this.contentEl;
    container.empty();
    container.addClass("paper-reading-workbench-source-view");
    const state = this.viewState || {};
    const zotero = state.zotero || {};
    container.createEl("h2", { text: state.title || "Zotero Source" });
    const meta = container.createDiv({ cls: "paper-reading-workbench-source-meta" });
    meta.createEl("div", { text: `Zotero key: ${state.key || "-"}` });
    meta.createEl("div", { text: `Zotero local status: ${zotero.status || "unavailable"}` });
    if (zotero.bestAttachmentPath) meta.createEl("div", { text: `Attachment path: ${zotero.bestAttachmentPath}` });
    if (state.metadataSource) meta.createEl("div", { text: `Metadata: ${state.metadataSource}` });
    const links = container.createDiv({ cls: "paper-reading-workbench-source-links" });
    links.createEl("a", { text: "Open Zotero item", href: zotero.itemUri || `zotero://select/library/items/${state.key || ""}` });
    if (zotero.bestAttachmentUri) {
      links.createEl("a", { text: "Open Zotero PDF attachment", href: zotero.bestAttachmentUri });
    }
    if (state.pdfUrl) {
      links.createEl("a", { text: "Open arXiv PDF fallback", href: state.pdfUrl });
    }
    if (state.arxivUrl) {
      links.createEl("a", { text: "Open arXiv page", href: state.arxivUrl });
    }
    const actions = container.createDiv({ cls: "paper-reading-workbench-source-actions" });
    const openZoteroButton = actions.createEl("button", { text: "打开 Zotero PDF 附件" });
    openZoteroButton.addEventListener("click", async () => {
      if (state.key) await this.plugin.openZoteroPdfForSource(state);
    });
    const translateButton = actions.createEl("button", { text: "生成/更新中文翻译" });
    translateButton.addEventListener("click", async () => {
      if (state.key) await this.plugin.runTranslation([state.key]);
    });
    const diagramButton = actions.createEl("button", { text: "打开/生成知识图" });
    diagramButton.addEventListener("click", async () => {
      if (state.key) await this.plugin.openOrGenerateKnowledgeDiagram(state.key, state.diagramPath);
    });
    if (state.entryPath) {
      const entryLink = links.createEl("a", { text: "Open Zotero source note" });
      entryLink.addEventListener("click", async () => {
        const file = this.app.vault.getAbstractFileByPath(state.entryPath);
        if (file instanceof TFile) await this.leaf.openFile(file);
      });
    }
    if (state.diagramPath) {
      const diagramLink = links.createEl("a", { text: "Open knowledge diagram file" });
      diagramLink.addEventListener("click", async () => {
        const file = this.app.vault.getAbstractFileByPath(state.diagramPath);
        if (file instanceof TFile) await this.leaf.openFile(file);
      });
    }
    if (state.pdfUrl) {
      const iframe = container.createEl("iframe", {
        attr: {
          src: state.pdfUrl,
          title: "Paper PDF fallback",
        },
      });
      iframe.addClass("paper-reading-workbench-pdf-frame");
    } else {
      container.createEl("p", {
        text: "Open the original PDF in Zotero using the links above. No arXiv PDF fallback was found in local daily records.",
      });
    }
  }
}

class PaperWorkbenchControlView extends ItemView {
  constructor(leaf, plugin) {
    super(leaf);
    this.plugin = plugin;
    this.keyInput = null;
    this.statusEl = null;
  }

  getViewType() {
    return VIEW_TYPE_PAPER_CONTROL;
  }

  getDisplayText() {
    return "Paper Workbench";
  }

  getIcon() {
    return "book-open";
  }

  async onOpen() {
    await this.render();
  }

  async render() {
    const container = this.contentEl;
    container.empty();
    container.addClass("paper-workbench-control-view");

    container.createEl("h2", { text: "Paper Workbench" });
    const hint = container.createEl("p", { text: "当前笔记有 zotero_key 时会自动识别；也可以手动输入 Zotero key。" });
    hint.addClass("paper-workbench-control-hint");

    const currentKey = await this.plugin.resolveCurrentZoteroKey();
    const row = container.createDiv({ cls: "paper-workbench-key-row" });
    this.keyInput = row.createEl("input", {
      type: "text",
      value: currentKey,
      placeholder: "Zotero key, e.g. <ZOTERO_KEY>",
    });
    const refreshButton = row.createEl("button", { text: "刷新" });
    refreshButton.addEventListener("click", async () => {
      const key = await this.plugin.resolveCurrentZoteroKey();
      this.keyInput.value = key;
      this.setStatus(key ? `已识别当前 key: ${key}` : "当前笔记没有 zotero_key。");
    });

    const actions = container.createDiv({ cls: "paper-workbench-actions" });
    this.addAction(actions, "打开工作台", async (key) => {
      this.setStatus(`正在打开工作台: ${key}`);
      await this.plugin.openWorkbenchForKey(key);
      this.setStatus(`已打开工作台: ${key}`);
    });
    this.addAction(actions, "打开 Zotero 原文", async (key) => {
      this.setStatus(`正在请求 Zotero: ${key}`);
      await this.plugin.openZoteroItemForKey(key);
      this.setStatus(`已请求 Zotero 打开: ${key}`);
    });
    this.addAction(actions, "生成翻译", async (key) => {
      this.setStatus(`正在启动翻译: ${key}`);
      await this.plugin.runTranslation([key]);
      this.setStatus(`翻译任务已启动: ${key}`);
    });
    this.addAction(actions, "打开/生成知识图", async (key) => {
      this.setStatus(`正在打开或生成知识图: ${key}`);
      await this.plugin.openOrGenerateKnowledgeDiagram(key);
      this.setStatus(`知识图已打开或生成任务已启动: ${key}`);
    });

    this.statusEl = container.createEl("div", { text: currentKey ? `当前 key: ${currentKey}` : "等待选择文献笔记或输入 Zotero key。" });
    this.statusEl.addClass("paper-workbench-status");
  }

  addAction(parent, label, callback) {
    const button = parent.createEl("button", { text: label });
    button.addEventListener("click", async () => {
      const key = this.currentKey();
      if (!key) {
        this.setStatus("请先输入或识别 Zotero key。");
        return;
      }
      try {
        await callback(key);
      } catch (error) {
        this.setStatus(`${label} 失败: ${error.message}`);
      }
    });
  }

  currentKey() {
    return String((this.keyInput && this.keyInput.value) || "").trim().toUpperCase();
  }

  setStatus(message) {
    if (this.statusEl) this.statusEl.setText(message);
    new Notice(message);
  }
}

class ZoteroKeyModal extends Modal {
  constructor(app, onSubmit) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("paper-reading-workbench-modal");
    contentEl.createEl("h2", { text: "Open paper workbench" });
    const input = contentEl.createEl("input", {
      type: "text",
      placeholder: "Zotero key, e.g. <ZOTERO_KEY>",
    });
    input.addEventListener("keydown", async (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        const key = input.value.trim().toUpperCase();
        this.close();
        await this.onSubmit(key);
      }
    });
    new Setting(contentEl).addButton((button) => {
      button.setButtonText("Open").setCta().onClick(async () => {
        const key = input.value.trim().toUpperCase();
        this.close();
        await this.onSubmit(key);
      });
    });
    input.focus();
  }
}

class PaperReadingWorkbenchSettingTab extends PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Paper Reading Workbench" });
    new Setting(containerEl)
      .setName("Translation max concurrency")
      .setDesc(`Hard-capped at ${MAX_TRANSLATION_CONCURRENCY}.`)
      .addText((text) => {
        text.setValue(String(this.plugin.settings.translationMaxConcurrency)).onChange(async (value) => {
          this.plugin.settings.translationMaxConcurrency = clampConcurrency(value);
          await this.plugin.saveData(this.plugin.settings);
        });
      });
    new Setting(containerEl)
      .setName("Translation timeout seconds")
      .addText((text) => {
        text.setValue(String(this.plugin.settings.translationTimeoutSec)).onChange(async (value) => {
          const parsed = Number.parseInt(value, 10);
          this.plugin.settings.translationTimeoutSec = Number.isFinite(parsed) && parsed > 0 ? parsed : 1200;
          await this.plugin.saveData(this.plugin.settings);
        });
      });
    new Setting(containerEl)
      .setName("Gemini model")
      .addText((text) => {
        text.setValue(String(this.plugin.settings.translationModel)).onChange(async (value) => {
          this.plugin.settings.translationModel = value.trim() || "gemini-3.1-pro-preview";
          await this.plugin.saveData(this.plugin.settings);
        });
      });
    new Setting(containerEl)
      .setName("Python command")
      .addText((text) => {
        text.setValue(String(this.plugin.settings.pythonCommand)).onChange(async (value) => {
          this.plugin.settings.pythonCommand = value.trim() || "python";
          await this.plugin.saveData(this.plugin.settings);
        });
      });
    new Setting(containerEl)
      .setName("Open control panel on startup")
      .setDesc("Shows the clickable Paper Workbench panel when Obsidian starts.")
      .addToggle((toggle) => {
        toggle.setValue(Boolean(this.plugin.settings.openControlPanelOnStartup)).onChange(async (value) => {
          this.plugin.settings.openControlPanelOnStartup = value;
          await this.plugin.saveData(this.plugin.settings);
        });
      });
  }
}

function clampConcurrency(value) {
  const parsed = Number.parseInt(String(value), 10);
  if (!Number.isFinite(parsed)) return MAX_TRANSLATION_CONCURRENCY;
  return Math.max(1, Math.min(MAX_TRANSLATION_CONCURRENCY, parsed));
}

async function fetchWithTimeout(url, timeoutMs) {
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    window.clearTimeout(timer);
  }
}

function readFrontmatterField(text, key) {
  const match = text.match(new RegExp(`^${key}:\\s*\"?([^\"\\n]+)\"?\\s*$`, "m"));
  return match ? match[1].trim() : "";
}

function normalizeWords(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .split(/\s+/)
    .filter(Boolean);
}

function renderCandidateChineseBrief(item) {
  const lines = [];
  lines.push(`- 题名：${item.title || "未命名候选"}`);
  lines.push(`- 一句话判断：${item.claim_compression || item.hypothesis || "需要人工补充判断。"}`);
  if (item.engineering_pathology) lines.push(`- 工程病灶：${item.engineering_pathology}`);
  if (item.mechanism) lines.push(`- 核心机制：${item.mechanism}`);
  if (item.non_obvious_claim) lines.push(`- 非显然性主张：${item.non_obvious_claim}`);
  if (item.strongest_baseline) lines.push(`- 最强 baseline：${item.strongest_baseline}`);
  if (item.killer_experiment) lines.push(`- 杀手实验：${item.killer_experiment}`);
  if (item.reviewer_pre_mortem || item.reviewer_kill_shot) {
    lines.push(`- 审稿人预反驳：${item.reviewer_pre_mortem || item.reviewer_kill_shot}`);
  }
  if (item.rescue_mutation || item.rescue_signal) {
    lines.push(`- 可救路径：${item.rescue_mutation || item.rescue_signal}`);
  }
  return lines;
}

function escapeYaml(value) {
  return String(value || "").replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}
