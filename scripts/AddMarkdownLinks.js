module.exports = async ({ app, quickAddApi }) => {

    const file = app.workspace.getActiveFile();
    if (!file) {
        new Notice("Open a note first");
        return;
    }

    // ---------- TYPE ----------
    const type = await quickAddApi.inputPrompt("Type");
    if (!type) return;

    // ---------- RELATION TYPE ----------
    const relationType = await quickAddApi.inputPrompt("Relation type");
    if (!relationType) return;

    // ---------- LINKS ----------
    const folderPath = "content/";

    const files = app.vault.getMarkdownFiles()
        .filter(f => f.path.startsWith(folderPath));

    const display = files.map(f => f.basename);
    const values = files.map(f => f.basename);

    const options = [...display, "Type manually"];
    const optionValues = [...values, "manual"];

    let links = await quickAddApi.suggester(options, optionValues);
    if (!links) return;

    if (links === "manual") {
        links = await quickAddApi.inputPrompt("Enter links (comma separated)");
        if (!links) return;
    }

    const linksArray = links.includes(",")
        ? links.split(",").map(l => l.trim().replace(".md",""))
        : [links.replace(".md","")];

    // ---------- FRONTMATTER ----------
    await app.fileManager.processFrontMatter(file, (fm) => {

        let changed = false;

        // TYPE
        if (!fm.type) {
            fm.type = type;
            changed = true;
        }

        // RELATION FIELD
        if (!fm[relationType]) {
            fm[relationType] = [];
            changed = true;
        }

        if (!Array.isArray(fm[relationType])) {
            fm[relationType] = [fm[relationType]];
            changed = true;
        }

        linksArray.forEach(l => {
            const linkValue = `[[${l}]]`;
            if (!fm[relationType].includes(linkValue)) {
                fm[relationType].push(linkValue);
                changed = true;
            }
        });

        // CREATED (only once)
        if (!fm.created) {
            fm.created = window.moment().format("YYYY-MM-DD");
            changed = true;
        }

        // 🔥 SAFE REORDER (only if something changed)
        if (changed && fm.created) {

            const ordered = { created: fm.created };

            Object.keys(fm).forEach(key => {
                if (key !== "created") {
                    ordered[key] = fm[key];
                }
            });

            // safe overwrite (minimal mutation)
            for (const key in fm) delete fm[key];
            Object.assign(fm, ordered);
        }
    });
};