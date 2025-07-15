ScriptName Samples:EventScript

CustomEvent MyEvent

Struct MyEventArgs
	bool MyBool = false
	int MyInt = 0
	float MyFloat = 0.0
	string MyString = ""
	ScriptObject MyScript = none
EndStruct

Function Send()
	MyEventArgs e = new MyEventArgs
	e.MyBool = true
	e.MyInt = 24
	e.MyFloat = 123.123
	e.MyString = "Hello World!"
	e.MyScript = Game.GetPlayer()
	var[] arguments = new var[3]
	arguments[0] = e
	arguments[1] = Utility.GameTimeToString(Utility.GetCurrentGameTime())
	arguments[2] = Utility.GetCurrentStackID()
	self.SendCustomEvent("MyEvent", arguments)
EndFunction

Event Samples:EventScript.MyEvent(Samples:EventScript sender, var[] arguments)
	{The custom event handler.}
	MyEventArgs e = arguments[0] as MyEventArgs
	string time = arguments[1] as string
	int stack = arguments[2] as int
	Debug.TraceSelf(self, "Samples:EventScript", "sender:"+sender + ", e:"+e+ ", time:"+time+ ", stack:"+stack)
EndEvent
