def adventure_game():
    print("🌍 Welcome to the Adventure Game!")
    print("You wake up in a mysterious forest. Paths stretch out before you...")

    choice1 = input("Do you go LEFT towards the river, or RIGHT towards the mountains? (left/right): ").lower()

    if choice1 == "left":
        print("\nYou walk to the river. The water is clear and cold.")
        choice2 = input("Do you DRINK the water or FOLLOW the river downstream? (drink/follow): ").lower()

        if choice2 == "drink":
            print("\nThe water refreshes you, but suddenly you feel dizzy... You faint. Game Over.")
        elif choice2 == "follow":
            print("\nYou follow the river and discover a hidden village. The villagers welcome you. You win!")
        else:
            print("Invalid choice. The forest swallows you. Game Over.")

    elif choice1 == "right":
        print("\nYou climb towards the mountains. The path is steep and rocky.")
        choice2 = input("Do you ENTER a dark cave or CONTINUE climbing? (enter/continue): ").lower()

        if choice2 == "enter":
            print("\nInside the cave, you find treasure... but a dragon guards it! Game Over.")
        elif choice2 == "continue":
            print("\nYou reach the mountain peak and see the whole land. You are free! You win!")
        else:
            print("Invalid choice. The mountain crumbles beneath you. Game Over.")

    else:
        print("Invalid choice. You wander aimlessly until night falls. Game Over.")

# Run the game
adventure_game()
