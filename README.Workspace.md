## VS Code: Workspace Settings
This project enforces some workspace settings to support features and ensure consistency.


### Python Indentation
The Python code uses spaced indentation with a tab size of 4.

@`\.vscode\settings.json`
```json
{
	"[python]": {
		"editor.detectIndentation": false,
		"editor.insertSpaces": true,
		"editor.tabSize": 4
	}
}
```

### Python Strict Annotations
This project uses strict type checking and annotation.

@`\.vscode\settings.json`
```json
{
	"python.analysis.typeCheckingMode": "strict"
}
```


### Papyrus Compiler
The VS Code build tasks use the `${config:papyrus.compiler.path}` setting to compile imported scripts into Papyrus assembly.
This is done to ensure the compiler import dependencies are valid for each Papyrus project.
Create a new `*.code-workspace` on the root directory and add the following setting.
Avoid committing your own local `papyrus.compiler.path` setting to the repository.

@`\UESP.Wiki.code-workspace`
```json
{
  "settings":
  {
    "papyrus.compiler.path": "C:\\Starfield\\Tools\\Papyrus Compiler\\PapyrusCompiler.exe"
  }
}
```

### Papyrus Indentation
The Papyrus code uses tabbed indentation.

@`\.vscode\settings.json`
```json
{
	"[papyrus]": {
		"editor.detectIndentation": false,
		"editor.insertSpaces": false
	}
}
```


## VS Code: Workspace Tasks
The VS Code configurations provide a default build task for compiling Papyrus source code into Papyrus assembly code.
Running the assembler on the source code imports will ensure the source code is valid and all dependencies are present.

The default build task is a task group called `Assemble All` which will starts a build task for each Papyrus import.
The default key binding for the default build task is **CTRL + SHIFT + B**.

Run this task when any Papyrus import changes.
