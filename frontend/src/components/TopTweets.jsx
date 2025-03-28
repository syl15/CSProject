import React from 'react'
import TweetBox from './TweetBox';


export default function TopTweets() {
  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 h-[25rem] w-full">
        <div className="border-b-1 border-[#D4D4D4]">
            <h3 className="pb-2">Top Tweets</h3>
        </div>
        <div className="flex flex-col pt-4 gap-y-3 overflow-y-scroll scrollbar">
            <TweetBox/>
            <TweetBox/>
            <TweetBox/>
        </div>
    </div>
  );
}
