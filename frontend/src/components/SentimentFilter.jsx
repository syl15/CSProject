import * as React from "react";
import { Collapsible } from "radix-ui";
import {
	CaretDownIcon, CheckIcon, Cross2Icon, RowSpacingIcon
} from "@radix-ui/react-icons";
import { useState } from "react";

export default function SentimentFilter({positiveSelected}) {
    const [open, setOpen] = useState(false);
	const [currSelection, setCurrSelection] = useState("Overall Sentiment");

	const allSelection = () => {
		setCurrSelection("Overall Sentiment");
		setOpen(false);
	}

	const positiveSelection = () => {
		setCurrSelection("Positive");
		setOpen(false);
	}

	const neutralSelection = () => {
		setCurrSelection("Neutral");
		setOpen(false);
	}

	const negativeSelection = () => {
		setCurrSelection("Negative");
		setOpen(false);
	}

	return (
        
		<Collapsible.Root
			className="relative"
			open={open}
			onOpenChange={setOpen}
		>
		<Collapsible.Trigger className="flex flex-row justify-center items-center gap-x-2 border border-[#D4D4D4] rounded-md bg-white">
			{currSelection}
			{open ? <Cross2Icon /> : <CaretDownIcon />}
		</Collapsible.Trigger>
       
        
		<Collapsible.Content className="flex flex-col flex-start border border-[#D4D4D4] rounded-md gap-y-1 text-left p-4 mt-3 ">
			<div className="hover:bg-[#F6F6F6] py-1 pl-2 rounded-md" onClick={() => allSelection()}>
				<span className="Text">All</span>
			</div>
			<div className="hover:bg-[#F6F6F6] py-1 pl-2 rounded-md" onClick={() => positiveSelection()} onChange={positiveSelected}>
				<span className="Text">Positive</span>
			</div>
			<div className="hover:bg-[#F6F6F6] py-1 pl-2 rounded-md" onClick={() => neutralSelection()}>
				<span className="Text">Neutral</span>
			</div>
            <div className="hover:bg-[#F6F6F6] py-1 pl-2 rounded-md" onClick={() => negativeSelection()}>
				<span className="Text">Negative</span>
			</div>
			</Collapsible.Content>
		</Collapsible.Root>
    );
};
