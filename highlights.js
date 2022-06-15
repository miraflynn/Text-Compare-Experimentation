/*
Created 6/7 by Mira Flynn for Pfizer GCS
This code is intended to take 2 strings and output 2 html-formatted strings highlighting differences between them.
The HTML for this is in a separate HTML file with a form with 2 string inputs, and 2 divs for the output results.
The CSS is in a separate CSS file defining a highlight color for correct letters and incorecct letters.

Note: I think it might be possible to inject some HTML via the form inputs. Depending on how widely this is used, someone might want to spend a bit considering that possibility. TBH not sure if it's possible or not, input sanitization isn't something I know much about.
*/

/*
findDiff()
Take 2 strings and compare them. Highlight differences and return highlighted HTML string. This is the overall control function.
Inputs: none
Returns: length 2 array of strings
*/
function findDiff(){
    var str1 = getInputValue("str1"); // Get the 2 string values
    var str2 = getInputValue("str2");
    console.log(str1);
    console.log(str2);
    // console.log(str1.split(/(\s)/));
    // Wow I hate regexes
    // console.log(str1.split(/(?<=[^A-Za-z0-9])|(?=[^A-Za-z0-9])/)); // This regex splits at any non-alphanumeric character, maintaining spaces and punctuation in the split.
    // console.log(str1.split(/([^A-Za-z0-9]+)/)); // This regex splits at one or more non-alphanumeric character, meaning that it will group non-alphanumeric characters.
    // // For reasons I don't fully understand, it adds an "" at the end of the split array if there's a special character at the end
    // console.log("a  b  ".split(/(\s)/));


    // var arr1 = getChars(str1); // Get the characters of each string
    // var arr2 = getChars(str2);

    var arr1 = getWords(str1);
    var arr2 = getWords(str2);

    var formattedStrings = formatDiffs(arr1, arr2); // Calculate and format the strings into HTML showing the differences
    var formattedStr1 = formattedStrings[0]; // extract each individual string
    var formattedStr2 = formattedStrings[1];
    console.log(formattedStr1);
    console.log(formattedStr2);
    setHTMLContent("results1", formattedStr1); // Format the HTML output box with the string
    setHTMLContent("results2", formattedStr2);
    return formattedStrings;
}

/*
getInputValue(name)
Gets and returns the value of the form input with id "id"
Inputs: 
    id: string
Returns: string
*/
function getInputValue(id){
    if(typeof(id) != "string"){ // type check the id as a string
        throw new TypeError("getInputValue id must be a string", "highlights.js");
    }
    return String(document.getElementById(id).value);
}


/*
getChars(str)
Takes str and splits into individual characters.
Inputs:
    str: string
Returns: array of characters
*/

// For future iterations of this, possibly replace with getting words and then comparing words? That way you could more easily differentiate where a word was added or removed.
function getChars(str){
    if(typeof(str) != "string"){ // type check the input as a string
        throw new TypeError("getChars str must be a string", "highlights.js");
    }
    return str.split('');
}

/*
getWords(str)
Takes str and splits into "words". Splits into each segment of alphanumeric characters and each segment of non-alphanumeric characters
For example:
abc def. ghi -> ["abc", " ", "def", ". ", "ghi"]
Inputs:
    str: string
Returns: array of strings
*/
function getWords(str){
    if(typeof(str) != "string"){ // type check the input as a string
        throw new TypeError("getWords str must be a string", "highlights.js");
    }
    var wordsArr = str.split(/([^A-Za-z0-9]+)/);
    // This regex isn't perfect. If the last character is a non-alphanumeric character, it has an empty string at the end of the array.
    // I despise regexes so much.
    if(wordsArr[wordsArr.length - 1] == ""){
        wordsArr.pop()
    }
    return wordsArr;
}


/*
formatDiffs(arr1, arr2)
Takes 2 arrays and compares character by character. Constructs 2 HTML formatted strings showing which characters are different.
Inputs:
    arr1: array
    arr2: array
Returns: length 2 array of strings
*/
function formatDiffs(arr1, arr2){
    var formattedStr1 = ""; // Empty formatted strings to build onto
    var formattedStr2 = "";

    if(!Array.isArray(arr1)){ // Type check arr1 as array
        throw new TypeError("formatDiffs arr1 must be an array", "highlights.js");
    }
    if(!Array.isArray(arr2)){ // Type check arr2 as array
        throw new TypeError("formatDiffs arr2 must be an array", "highlights.js");
    }
    // TODO: Check that arrays are full of strings. Technically, it can actually work for any type, but it really should be strings.

    for(let i=0; i < Math.max(arr1.length, arr2.length); i++){ // Iterate over each character of both strings
        if(arr1[i] == arr2[i]){
            formattedStr1 = formattedStr1 + "<span class='same'>"+arr1[i]+"</span>"; // If characters equal, put both characters in span of class same
            formattedStr2 = formattedStr2 + "<span class='same'>"+arr2[i]+"</span>";
        } else { // If characters not equal, one character could be undefined on the shorter input
            if(typeof(arr1[i]) !== "undefined"){ // Only add this character if not undefined
                formattedStr1 = formattedStr1 + "<span class='different'>"+arr1[i]+"</span>";
            }
            if(typeof(arr2[i]) !== "undefined"){
                formattedStr2 = formattedStr2 + "<span class='different'>"+arr2[i]+"</span>";
            }
        }
    }
    return([formattedStr1, formattedStr2]);
}


/*
setHTMLContent(id, content)
Takes an element id and html string. Sets id element inner html to content.
Inputs:
    id: string
    content: string
Returns: none
*/

// NOTE: This might be questionable coding practice, as I think someone could inject some questionable HTML via the inputs.
function setHTMLContent(id, content){
    if(typeof(id) != "string"){ // Type check id as string
        throw new TypeError("setHTMLContent id must be a string", "highlights.js");
    }
    if(typeof(content) != "string"){ // Type check content as string
        throw new TypeError("setHTMLContent content must be a string", "highlights.js");
    }
    // TODO: Check that element returned is actually a div or something that can have inner html
    div = document.getElementById(id);
    div.innerHTML = content;
}