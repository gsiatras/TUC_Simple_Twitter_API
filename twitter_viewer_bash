%%file twitterViewerEditor.sh
#!/bin/bash
declare -a list=()
id=0

print_menu() {
    echo "   Press: c.To create a new Tweet.'
        'r.To read tweet. (usage: r tweet_number)'
        'u.To update tweet. (usage: u tweet_number)'
        'd.To delete tweet.'
        '$.To read last tweet.'
        '-.To read previous tweet from the current one.'
        '+.To read next tweet from the current one.'
        '=.To print current tweet.'
        'q.To quit without save.'
        'w.To write file to disk.'
        'x.To exit and save."
}

readfile() {
    while IFS= read  -a line
    do
        ##echo "$line"
        #echo -e "\n"
        list+=("$line")
        ##echo ${list[${#list[@]} - 1]}

    done < "$1"
}


setTweetId() {
    last=$((${#list[@]} - 1))
    if ((0 < $1 < last))
    then

        id=$1
    else
        echo -e "Tweet not found (given id is too big or <0)\n"
    fi
}

lowerTweetId() {
    if (($id > 0))
    then
        let "id--"
    else
        echo -e "First tweet"
    fi
}

increaseTweetId() {
    last=$((${#list[@]} - 1))
    if ((id < $last))
    then
        let "id++"
    else
        echo -e "Last tweet"
    fi
}

setTweetIdtoLast() {
    echo -e $((${#list[@]} - 1))
    id=$((${#list[@]} - 1))
}

createTweet() {
    echo -n "Tweet Text:"
    read text
    list+=("$text")
    id=$((${#list[@]} - 1))
}

updateTweet() {
    last=$((${#list[@]} - 1))
    if ((0 < $1 < last))
    then
        echo -n "Tweet new Text:"
        read text
        list[$1]="$text"
        id=$1
    else
        echo -e "Tweet not found (given id is too big or <0)\n"
    fi
}

saveToFile() {
    truncate -s 0 "/home/gsiatras/Documents/tweetsmall.txt"
    for line in "${list[@]}"; do
        echo "$line" >> "/home/gsiatras/Documents/tweetsmall.txt";
    done
}

printTweet() {
    echo -e "Tweet Id: $id\t Text: ${list[$id]}"
}


main() {
    readfile "/home/gsiatras/Documents/tweetsmall.txt"


    print_menu


    while true
    do
    echo -n "Enter:"
    read input
    case ${input:0:1} in

        c)
           createTweet
            ;;

        r)
            setTweetId ${input:1:6}
            printTweet
            echo ${list[${input:1:6}]}
            ;;

        u)
            updateTweet ${input:1:6}
            ;;

        d)
            echo -n "d"
            ;;

        $)
            setTweetIdtoLast
            printTweet
            ;;

        -)
            lowerTweetId
            printTweet
            ;;

        +)
            increaseTweetId
            printTweet
            ;;

        =)
            printTweet
            ;;

        q)
            echo -n "Exit without save"
            exit
            ;;

        w)
            saveToFile
            ;;

        x)
            saveToFile
            echo -n "Exit after save"
            exit
            ;;

        *)
        ;;
    esac
    done
    }




main
