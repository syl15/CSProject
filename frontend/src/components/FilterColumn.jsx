import * as React from "react";
import Searchbar from "./Searchbar";
import { MixerHorizontalIcon } from "@radix-ui/react-icons";
import DisasterTypeFilter from "./DisasterTypeFilter";
import SentimentFilter from "./SentimentFilter";

export default function FilterColumn() {
	return(
        <div className="relative flex flex-col flex-start mt-15 pr-40 gap-y-6">
            <Searchbar/>   
            <p className="text-left text-md flex flex-row items-center gap-x-3"><MixerHorizontalIcon width={20} height={20}/>  Filter by: </p>
            <div className="md:absolute md:mt-29 flex flex-col gap-y-4 ">
                <SentimentFilter/>
                <DisasterTypeFilter/>
            </div>
        </div>  
    );
};
