# UESP.Wiki
Some automation for https://starfieldwiki.net/ MediaWiki contributions.

### TODO
- The `Template:Script_Object_Summary` `extends` field needs to support breadcrumb links for inheritance.
- Parser does not handle properties with default value field initializers. See `Actor.wiki` and `ObjectReference.wiki`.
- The `ScriptObject.psc` should explicitly list `Nothing` as it's `Extends`, but it should not be a page link.
- Fix parser return type for functions. Functions that have no return type should NOT use `none`. It should be blank or use `void`.

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
https://starfieldwiki.net/wiki/Template:Script_Member_Summary
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
