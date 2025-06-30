ScriptName Samples:Script Extends Samples:NativeScript Conditional Hidden

;/
    This is a multi-line comment block that documents
    this sample script showing various Papyrus features
/;

; Import statements would go here
Import Debug
Import Game
Import Utility

; Custom structure definition
Struct ItemData
    string Name
    int Count = 0
    bool IsQuestItem = false
EndStruct

; Properties with various flags
string Property Description = "Default description" Auto
Actor Property PlayerRef Auto Mandatory
{The player reference - this is a documentation block for the property}
int Property Counter = 0 Auto Hidden
ItemData[] Property Items Auto

; Global variables at script level
bool isActive = false
float fTimer = 1.5

; Events
Event OnInit()
    Debug.Trace("Sample script initialized")
    isActive = true
    StartTimer(fTimer)
    MyFunctionNative(fTimer)
EndEvent

Event OnTimer(int aiTimerID)
    if(isActive)
        Counter += 1
        Debug.Trace("Timer fired: " + Counter)
        StartTimer(fTimer)
        MyFunctionNative(fTimer)
    endif
EndEvent

Event OnActivate(ObjectReference akActionRef)
    if(akActionRef == PlayerRef)
        GoToState("Active")
    endif
EndEvent

; Functions with different return types and parameters
int Function AddItems(string itemName, int amount, bool abSilent = false)
    if(amount <= 0)
        return 0
    endif

    ItemData newItem = new ItemData
    newItem.Name = itemName
    newItem.Count = amount

    if(!abSilent)
        Debug.Notification("Added " + amount + " " + itemName)
    endif

    return amount
EndFunction

; States for state-based behavior
State Active
    Event OnBeginState(string asOldState)
        Debug.Trace("Entered Active state from " + asOldState)
    EndEvent

    Event OnActivate(ObjectReference akActionRef)
        ; Override the default event in this state
        Debug.Notification("Already active!")
        GoToState("")
    EndEvent

    Event OnEndState(string asNewState)
        Debug.Trace("Exiting Active state to " + asNewState)
    EndEvent
EndState


Auto State Inactive
    Event OnBeginState(string asOldState)
        Debug.Trace("Entered Inactive state from " + asOldState)
    EndEvent

    Event OnActivate(ObjectReference akActionRef)
        Debug.Notification("Activating from Inactive state")
        GoToState("Active")
    EndEvent

    Event OnEndState(string asNewState)
        Debug.Trace("Exiting Inactive state to " + asNewState)
    EndEvent
EndState

; Global function
bool Function IsPlayerNearby(ObjectReference this) Global
    Actor player = Game.GetPlayer()
    return player && (this.GetDistance(player) < 200.0)
EndFunction
