import React from 'react'


export default function TweetBox({tweetObj}) {
  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-xl p-5 mr-5">
      <a href={tweetObj.link} target="_blank" rel="noopener noreferrer">
        <h4 className="text-md">{tweetObj.posterName}</h4>
        <p className="text-sm text-[#9D9D9D]">{tweetObj.username}</p>
        <div className="flex flex-start flex-wrap pt-4 text-wrap overflow-x-hidden">
            <p>{tweetObj.content}</p>
        </div>
      </a>
    </div>
  );
}
