import React from 'react'
import TweetBox from './TweetBox';
import ToolTip from './ToolTip';


export default function TopTweets({tweetsList}) {
  const paragraph = "Posts are related to the disaster and grouped by a clustering algorithm. Clustering may occasionally be inaccurate."
  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 h-[35rem] md:h-[25rem] w-full">
        <div className="border-b-1 border-[#D4D4D4] pb-2">
          <div className="flex flex-row gap-x-2 items-center justify-between">
            <h3>Posts</h3>
            <ToolTip paragraph={paragraph}/>
          </div>
        </div>
        
        
        {tweetsList ? (
          <div className="flex flex-col pt-4 gap-y-3 overflow-y-scroll scrollbar">
            {tweetsList.map((tweet, index) => (
              <TweetBox key={tweet.id || index} tweetObj={tweet} />
            ))}
          </div>
        ) : (
          <div className="flex flex-wrap justify-center items-center leading-80">No data</div>
        )}
            
       
    </div>
  );
}
