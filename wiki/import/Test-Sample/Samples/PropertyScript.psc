ScriptName Samples:PropertyScript Extends Samples:NativeScript

ObjectReference PropertyFullRef_Value
ObjectReference Property PropertyFullRef
    ObjectReference Function Get()
        return PropertyFullRef_Value
    EndFunction
    Function Set(ObjectReference value)
        PropertyFullRef_Value = value
    EndFunction
EndProperty


bool PropertyFullBool_Value

bool Property PropertyFullBool_GetOnly
    bool Function Get()
        return PropertyFullBool_Value
    EndFunction
EndProperty

bool Property PropertyFullBool_SetOnly
    Function Set(bool value)
        PropertyFullBool_Value = value
    EndFunction
EndProperty


int Property AutoIntProperty Auto
ObjectReference Property AutoObjectRefProperty Auto

float Property AutoReadOnlyFloatProperty = 41.5 AutoReadOnly
Form Property AutoReadOnlyFormProperty = none AutoReadOnly
