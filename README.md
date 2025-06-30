# UESP.Wiki
Some automation for https://starfieldwiki.net/ MediaWiki contributions.

- [Reference for Script Objects](https://starfieldwiki.net/wiki/Starfield_Mod:Object_Scripts)
- [Reference for Editor Objects](https://starfieldwiki.net/wiki/Starfield_Mod:Form_Reference)


### VS Code: Workspace Settings
The VS Code build tasks use the `${config:papyrus.compiler.path}` setting to compile imported scripts into Papyrus assembly.
This is done to ensure the compiler import dependencies are valid for each Papyrus project.
Create a new `*.code-workspace` on the root directory and add the following setting.
Avoid committing your own local `papyrus.compiler.path` setting to the repository.
```json
{
  "settings":
  {
    "papyrus.compiler.path": "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Starfield\\Tools\\Papyrus Compiler\\PapyrusCompiler.exe"
  }
}
```


### TODO
- TODO: Remove all `# TODO:` from the project by doing them or migrating them to an issue tracker.
- Wiki: Finialize the output file structure and naming conventions.
- Wiki: Commit all wiki output to the repository for review by the UESP team & community.
  - Ensure the proposed page names, content, categories, and templates are sensible.
- Wiki: Page: Write struct member-variable information.
- Wiki: Page: Write property accessibility modifiers for auto/get/set.
- Wiki: Page: Write guard information.
- Wiki: Page: Write state information.
- Wiki: Page-Member: Write example sections that show remote syntax for events.
- Wiki: Page-Index: Write the number of undocumented scripts and members.
- Wiki: Page-Index: Fix uncounted statistics for member within states and groups.
- Wiki: Template: Find a way to transclude inherited members onto script pages. Preferably under collapsed headings.
- Papyrus: Parser: Support property get/set capabilities for non-auto properties.
- Papyrus: Parser: Support guards and guard flags on properties.
- Papyrus: Parser: Support struct member-variable information.
- Papyrus: Parser: Support remote event handler information.
- Papyrus: Parser: Create classes for `code.Comment` elements that split doc-string from gathered line comments.
- Papyrus: Parser: Support Papyrus line continuations where elements that are normally single line can span multiple lines.
- Papyrus: Parser: Support *script-import* definition information.
- Refactor `app.AppContext` and `app.PapyrusProject` with a new `papyrus.PapyrusContext` that manages scripts up to the *source-import* level.
