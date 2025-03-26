import React from 'react'


export default function TweetBox() {
  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-xl p-5 mr-5 w-auto">
        <h4 className="text-md">Jane Doe</h4>
        <p className="text-sm text-[#9D9D9D]">@janedoebluesky</p>
        <div className="flex flex-start flex-wrap pt-4 text-wrap overflow-x-hidden">
            <p>asdjflkajsdflajsdflakjsdlf;kajsdf;akjsd;fkajsdlfkasjdflkajsdfka;sldkfjla;ksdjfl;aksjdf;laksdjfaj
            dfasldfkjalsdjf
            aksdfjlaksjdfl dfasldfkjalsdjf dfasldfkjalsdjf dfasldfkjalsdjf
            dfasldfkjalsdjf
            dfasldfkjalsdjf</p>
        </div>
    </div>
  );
}
