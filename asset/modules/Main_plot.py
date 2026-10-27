def  wait_for_continue():
     input('\n[Press Enter to continue...]\n')
name = input('Enter you name: ').strip()

#define a function for the game to start

print(
     '''Attention all citizens. This is an emergency broadcast. A nuclear war has broken out. Seek for a desginated shelter near you immediately.
     I repeat, seek for a designated shelter near you immediately. Remember, DO NOT venture outside without protective gear, the rescue teams will arrive in seven days.'''
     )
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
print(name,':','''It's night time now, perhapsI should go to sleep.''')

wait_for_continue()
print('You sleep in the sleeing bag provided in the shelter. This is your day 1 in the shelter.')
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


