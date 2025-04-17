import * as React from "react";
import { Collapsible } from "radix-ui";
import {
	CaretDownIcon, CheckIcon, Cross2Icon, RowSpacingIcon
} from "@radix-ui/react-icons";
import { useState } from "react";

export default function DisasterTypeFilter() {
    const [open, setOpen] = useState(false);
	return (
		<Collapsible.Root
			className="CollapsibleRoot"
			open={open}
			onOpenChange={setOpen}
		>
	
		<Collapsible.Trigger className="flex flex-row justify-center items-center gap-x-2 border border-[#D4D4D4] rounded-md bg-white">
			Disaster Type
			{open ? <Cross2Icon /> : <CaretDownIcon />}
		</Collapsible.Trigger>

		<Collapsible.Content className="flex flex-col flex-start border border-[#D4D4D4] rounded-md gap-y-2 text-left p-4 mt-3">
			<div className="Repository">
				<span className="Text">All types</span>
			</div>
			<div className="Repository">
				<span className="Text">Hurricane</span>
			</div>
            <div className="Repository">
				<span className="Text">Flood</span>
			</div>
            <div className="Repository">
				<span className="Text">Earthquakes</span>
			</div>
            <div className="Repository">
				<span className="Text">Fire</span>
			</div>
			</Collapsible.Content>
		</Collapsible.Root>
    );

};
