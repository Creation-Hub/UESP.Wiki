ScriptName Samples:GuardScript Extends ObjectReference

Guard MyPropertyGuard
int property MyProperty1 = 2 Auto Hidden Conditional RequiresGuard(MyPropertyGuard)
int property MyProperty2 = 4 Auto Hidden Conditional RequiresGuard(MyPropertyGuard)
int property MyProperty3 = 8 Auto Hidden Conditional RequiresGuard(MyPropertyGuard)


Guard MyEventGuard ProtectsFunctionLogic

Event OnContainerChanged(ObjectReference akNewContainer, ObjectReference akOldContainer)
	Debug.TraceSelf(self, "OnContainerChanged", "akNewContainer:"+akNewContainer + ", akOldContainer:"+akOldContainer)
	LockGuard MyEventGuard
		; do work here
	EndLockGuard
EndEvent
