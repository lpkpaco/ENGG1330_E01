def  wait_for_continue():
     input('\n[Press Enter to continue...]\n')
name = input('Enter you name: ').strip()

#define a function for the game to start

print('''Attention all citizens. This is an emergency broadcast. A nuclear war has broken out. Seek for a desginated shelter near you immediately.\nI repeat, seek for a designated shelter near you immediately. Remember, DO NOT venture outside without protective gear, the rescue teams will arrive in seven days.''')
wait_for_continue()
print('DAY 1')
wait_for_continue()
print('(You lunge forward and bolt the heavy iron door of the shelter shut.\nBreatheless, you sit against the cold concrete wall,\nwatching the radiation indicator light flickering red outside the door window.)')
wait_for_continue()
print(name,':','Seven days... The government broadcast said the rescue teams will arrive in seven days. What I need to do is to survive until then. But the shelter is nearly empty...')
wait_for_continue()
print('(You inspect the corner the room, finding a yellow Hazmat suit hanging on the wall)')
wait_for_continue()
print(name,':','Well, at least I get this suit, I will be able to venture out to search for food and other necessities this week.')
wait_for_continue()
print('(You then find some biscuits, a bottle of water and a radio on the desk)')
wait_for_continue()
print(name,':','I guess I wiil have these biscuits as my meal today')
wait_for_continue()
print('(You then eat the biscuits and drink half of the water in the bottle)')
wait_for_continue()
print(name,':','''It's night time now, perhaps I should go to sleep.''')

wait_for_continue()
print('(You sleep in the sleeing bag provided in the shelter. This is your day 1 in the shelter.)')
wait_for_continue()

#print the game title

wait_for_continue()

print('Instructions for gameplay : Survive for 7 days and wait for rescue.\nTo survive, you need to keep the health bar above 0.\nIn a day, you can only scrap 3 resources including different food, water and medicine. They are randomly scattered across the map.\nSome resources require you to solve a puzzle to obtain while some can be obtained directly.\nReacting to random events upon return.')
wait_for_continue()
print('DAY 2')
wait_for_continue()
print(name,':','Sleeping in a sleeping bag is really unconfortable. But to survive, I have no choice.')
wait_for_continue()

#a function to pop out the map for the player to interact

#a function to call out random events or puzzle


input('\n[Click Enter to end day 2]\n') 
print('This is your day 2')
wait_for_continue()
print('DAY 3')

#map function

#puzzle/events function

input('\n[Click Enter to end day 3]\n')
print('This is your day 3')
wait_for_continue()
print('DAY 4')

#map function

#puzzle/events function

input('\n[Click Enter to end day 4]\n')
print('This is your day 4')
wait_for_continue()
print('DAY 5')

#map function 

#puzzle/events function

input('\n[Click Enter to end day 5]\n')
print('This is your day 5')
wait_for_continue()
print('DAY 6')

#map function
#The player shd go back to the shelter after he obtained the final tool in the map for fixing the radio 
#a function for, if the player has obtained all tools, unlock the hidden event -- interference on the airwaves,if not, a random event 

#The below should be under a if function after the puzzle for hidden event is finished and defined

#if radio_fixed:
    print('''Radio : If anyone is listening, the radiation and the nuclear...nuclear war are fake!\nThere's no such war and crisis.\nThis is a trap, an experimnent from the government.\nThe government is actually suffering from a slow-burning genetic crisis on the surface.\nThey used the nuclear panic to trick thousands of genetically compatible civilians into locking themselves in pristine isolators.\nDay 7 isn't an evacuation -- it's the harvest date when 'specimens' who maintained high health or suit integrity are selected for involuntary organ/tissue harvesting or gene-therapy research for the elite.''')
    wait_for_continue()
    print(name,':','''If this is real, there's no way I should wait for the 'rescue team' to come tomorrow.\nI have to find out what's the truth.''')
    wait_for_continue()
    print('(You walked out of the shelter, taking off the Hazmat suit, exposing yourself to the air without any protective gear.)')
    wait_for_continue()
    print('''(10 minutes passed, nothing happened, you didn't die because of the radiation.\nThe voice from the the radio was right, this is a lie.\n You know you shouldn't stay here any longer.)''')
    wait_for_continue()
    print(name,':','''I have to leave, I have to escaoe from this lie.\nI don't know where I should go, I only know that I have to leave this city as soon as possible.''')
    wait_for_continue()
    print('(You packed all the stuff you left in your bag.\nYou left the Hazmat suit in the shelter and started the wandering journey...)')
    input('\n[Click to end the game]\n') 
    print('GAME OVER - SURVIVED')
    print('HIDDEN ENDING : THE LAMB PREVENTS FROM SLAUGHTERING')
#else:    
    input('\n[Click Enter to end day 6]\n')
    print('This is your day 6')
    wait_for_continue()
    print('THE SEVENTH DAY')
    wait_for_continue()
    print(name,':','This is the day... Finally, the rescue team is here. I am saved.')
    print('(You patiently put on the Hazmat suit and wait inside. The shelter doors are opened by a group of people in full military biohazard gear.)')
    wait_for_continue()
    print('Rescue Team Leader : Subjected located. Vital signs are stable.\nCongraatulations, you made it to the seventh day, survivor.\nPlease step into the transport unit.')
    wait_for_continue()
    print('''(You are escorted into a covered truck. As the truck drives away.\nYou never sees what the world really looks like outside and you don't even know what's waiting for you after getting off this truck...''')
    print(name,':','''I survived. The suit protected me from the toxic wasteland.\nI don't know what's left of humanity, but I made it through the seven days.''')
    input('\n[Click to end the game]\n'
    print('GAME OVER - SURVIVED')
    print('ORDINARY ENDING : STANDARD SURVIVAL)
#print the game title
print('END')
#A function that return to the title menu
      
   






