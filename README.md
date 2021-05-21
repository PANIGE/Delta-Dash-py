# Delta Dash

Weird python mix between osu!taiko and Muse dash, with an osu!like mapping writing
This project is a School project, so i don't care about code perfectibility

###Sources
most of the sounds com from [osu!Lazer resources](https://github.com/ppy/osu-resources)
Sprites and some of sounds are found on random [osu! skins](https://osuskins.net/)
Font is Torus, ripped from [osu! web](https://github.com/ppy/osu-web) 



## Installation
use pip to install repositories

```bash
pip install --user -r requirements.txt
```

## Keys

There are a bunch of input available trough the game, that i'll list now

**_General_**
* Scrolling : Managing the main volume setting

**_Main Menu_**
* F2 : Pause the current song
* F3 : Unpause the current song
* F4 : Stop the current song
* F5 : Skip the current song
* Exit : Exit the game

**_Song Select_**
* Exit : Returns to main menu

**_Play_**

For the play menu, the input keys are chosen to fit small and large keyboard, since in most rythm games, the most spaced keys are the most confortable, for small keyboard, you want to use `F` and `K` but for large keyboards (with numpad) you'll mostly want to use `D` and `Num4` but both configs are always active
* `D` or `F` : Blue Key
* `J` or `Num4` : Red key

**_Ranking screen_**

* Escape : Returns to song select
* Exit : Returns to song select

## How To Play

The game contains basic mechanics in most of rythm games, Blue keys are for the upper portion of the screen, red ones are for the lower portion of the screen, your objective is to hit the circles that are coming at the right center of the screen, when it allign whith your overlay, you'll get +1 combo each note touched, but each note missed will reset your combo.

You win score by hitting perfectly the notes on screen and gaining some combo, more accurate you are with your hits, more points you win, you can know how you hit the note whith looking witch color is turning the combo indicator

* Light Blue : Perfect Hit
* Green : Good hit
* Yellow / orange : Inaccurrate (Meh) Hits
* Red : Miss

and more accurate you are, more points you win!

* Perfect : 300
* Good : 100
* Meh : 50
* Miss : 0

The hit score is multiplied by the combo, so more points you gain !
```
Score += Hit * combo
```

## Ranking
### Hits
At the right end of your map, you'll end on a screen, the Ranking screen, you'll get a bunch of info about your play, like your average accuracy. you'll also get the number of each hit you made
* Perfect : 100%
* Good : 66%
* Meh : 30%
* Miss : 0%

### Rank
And it will get the average accuracy of all notes, and will get you a Rank that are calculate on the percent of Perfect hits by all the notes in, and will get if you have any miss, having no miss is called Full Combo, because you have the max combo achievable (FC)

* 93+% FC = **_S_**
* 93+% = **_A_**
* 86+% FC = **_A_**
* 86+% = **_B_**
* 70+% FC = **_B_**
* 70+% = **_C_**
* 70-% FC = **_C_**
- 70-% = **_D_**

### Unstable Rate
Unstable rate is a more precise way to tell your accuracy, by gatting you in ms your delay and also giving you a graph to be more user friendly
UR is shown with number like this:
```markdown
Earliest hit / Average hit delay / Latest hit
```

## Maps statistics
* Note Speed : Speed of elements, higher this stat gets, faster the element will be on screen, can be confortable selecting map speed and difficulty
* Health Drain : how sensitive the life bar is, and how much a miss will cost to the life bar, higher this stat get, Each mistake will cost you more life
* Accuracy Needed : How much accuracy you'll need to have to hit the Perfect/good/Meh, higher this is, harder it gets to hit the 300
* Difficulty rating : A note given from the creator to get the global difficulty of a map, higher this is, harder the map is (Note this is unlinked from Normal / hard / insane diff) and is universal, since a 2 Rating is harder than a 1.5 Rating, no matter in which difficulty is it placed on

## Skinning
Any file in data can be replaced using the skins/user folder in .user without taking out the base files


[See Example Video here, it use old loading method so long loading isn't present anymore](https://youtu.be/Fd23WJmwj_E)
