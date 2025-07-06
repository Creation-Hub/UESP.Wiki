ScriptName Tests:LineContinuation
; A `\` character MUST be followed by a `\n` newline character.


Function Foo1(string arg1, string arg2, string arg3, \
	string arg4, string arg5, string arg6)
EndFunction


Function Foo2(\
	string arg1, \
	string arg2, \
	string arg3,\
	string arg4, \
	string arg5, \
	string arg6\
	)
EndFunction
