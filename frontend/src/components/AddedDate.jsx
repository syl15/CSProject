import React from 'react'
import ToolTip from './ToolTip';


export default function AddedDate({dateAdded}) {
    const paragraph = "The date the system detected and recorded this disaster or estimated by the LLM from its assigned posts."
    return (
        <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2">
            <div className="flex flex-row gap-x-2 items-center justify-between">
                <h3>Date Added</h3>
                <ToolTip paragraph={paragraph}/>
            </div>
            
            <h1 className="text-3xl font-bold">{dateAdded}</h1>
        </div>
    );
}
