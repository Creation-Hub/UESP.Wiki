# UESP.Wiki
Some automation for https://starfieldwiki.net/ MediaWiki contributions.

- [Reference for Script Objects](https://starfieldwiki.net/wiki/Starfield_Mod:Object_Scripts)
- [Reference for Editor Objects](https://starfieldwiki.net/wiki/Starfield_Mod:Form_Reference)

### TODO
- Fix parser return type for Papyrus functions with no return type. Functions that have no return type should NOT use `none`. It should be blank or use `void`.
- Generate member example sections that show remote syntax for events.
- Detect property get/set accessors in the parser.
- Collect Papyrus state information in the parser.

# Templates
The wiki templates used by this generator.

#### `Script_Object_Summary`
https://starfieldwiki.net/wiki/Template:Script_Object_Summary
```
<includeonly>
<cleantable>
{| class="wikitable infobox"
!colspan=2| {{{title|{{PAGENAME}}}}}
|-
![[SFM:Object_Scripts|Script]]
|{{{script|}}}
|-
!Extends
|{{{extends}}}
|-
![[SFM:Form_Reference|Editor]]
|{{{editor}}}
|-
!Base
|{{{base}}}
|-
![[SFM:Reference|Reference]]
|{{{reference|}}}
|}
</cleantable>
</includeonly>
<noinclude>{{/Doc}}</noinclude>
```

#### `Script_Object_Member_Summary`
https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
```
<includeonly>
<cleantable>
{| class="wikitable"
!colspan=2| {{{title|{{PAGENAME}}}}}
|-
![[SFM:Object_Scripts|Script]]
|{{{script|}}}
|-
!Name
|{{{name}}}
|-
!Kind
|{{{kind}}}
|-
!Flags
|{{{flags}}}
|-
!Returns
|{{{returns|}}}
|-
!Parameters
|{{{parameters|}}}
|-
!Documentation
|{{{documentation|}}}
|-
!Game Version
|{{{game_version|}}}
|}
</cleantable>
</includeonly>
<noinclude>{{/Doc}}</noinclude>
```

#### `Script_Member_Summary`
https://starfieldwiki.net/wiki/Template:Script_Member_Summary
```
```

#### `Script_DocGen_Meta`
https://starfieldwiki.net/wiki/Template:Script_DocGen_Meta
```
<includeonly>
<cleantable>
{| class="wikitable"
!colspan=2| Page Generation Meta
|-
!Generation Date
|{{{generator_date}}}
|-
!Generator Version
|{{{generator_version}}}
|-
!Game Version
|{{{game_version}}}
|-
!Game File
|{{{Game_file}}}
|}
</cleantable>
</includeonly>
<noinclude>{{/Doc}}</noinclude>
```
