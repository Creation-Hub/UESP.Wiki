ScriptName Tests:LineContinuation
{Testing for line continuations.}
; A `\` character MUST be followed by a `\n` newline character.

; This is the documentation line comment for `Foo`.
Function Foo(string arg1, string arg2, string arg3, string arg4, string arg5, string arg6)
	{This is the Papyrus doc-string for `Foo`.}
EndFunction


; This is the documentation line comment for `Foo1`.
Function Foo1(string arg1, string arg2, string arg3, 	  \
	string arg4, string arg5, string arg6)
	{This is the Papyrus doc-string for `Foo1`.}
EndFunction

; This is the documentation line comment for `Foo2`.
Function Foo2(\
	string arg1, \
	string arg2, \
	string arg3,\
	string arg4, \
	string arg5, \
	string arg6\
	)
	{This is the Papyrus doc-string for `Foo2`.}
EndFunction
