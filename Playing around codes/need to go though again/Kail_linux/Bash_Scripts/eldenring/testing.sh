#! /bin/bash
#by Wayne Stock
#created 2025-12-25
# just playing around with bash 
##################################################
# Varables




# Welcome Menu
echo ""
echo " Welcome Tarnished. PLease select you starting class:
1 - Samurai
2 - Prisoner
3 - Prophet"

read class

case $class in
    1)
        type="Samurai"
        hp=10
        attack=20
        ;;

    2) 
        type="Prisoner"
        hp=20
        attack=4
        ;;

    3)
        type="Prophet"
        hp=30
        attack=4
        ;;
esac
echo ""
echo "You chosen the $type class.  
Your HP is $hp 
Your attack is $attack."

sleep 3
echo ""
echo "You spawnd in "
#################################################



# 2 battle
echo ""
echo "Battle 2"
echo ""
echo "Boss battle.  Get scared.  It's Margit.  Pick a number between 0-9. (0-9)"
read tarnished
beast=$(( $RANDOM % 10 ))
if [[ $beast == $tarnished || $tarnished == "coffee" ]] then 
    echo "Beast VANQUISHED!!! Congrats fellow tarnished"
else
    echo "You Died"

fi
##################################################