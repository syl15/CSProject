import * as React from "react";
import { DropdownMenu } from "radix-ui";
import {
	CaretDownIcon, CheckIcon
} from "@radix-ui/react-icons";
import { useState } from "react";

export default function TimeFilter() {
	const [allTimeChecked, setallTimeChecked] = useState(false);
    const [oneYearChecked, setOneYearChecked] = useState(false);
    const [fiveYearChecked, setFiveYearChecked] = useState(false);
    const [tenYearChecked, setTenYearChecked] = useState(false);


	return (
		<DropdownMenu.Root className="-z-0">
            <DropdownMenu.Trigger className="flex flex-row items-center gap-x-2 border border-[#D4D4D4] rounded-xl">
                Time
                <CaretDownIcon/>
            </DropdownMenu.Trigger>

            <DropdownMenu.Portal>
                <DropdownMenu.Content 
                    className="w-40 max-h-60 border border-gray-300 rounded-md p-2"
                    sideOffset={5}>
                    <DropdownMenu.CheckboxItem
                        className="flex flex-row items-center gap-x-3 px-2 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm"
                        checked={allTimeChecked}
                        onCheckedChange={setallTimeChecked}
                    >
                        All Time
                        <DropdownMenu.ItemIndicator className="DropdownMenuItemIndicator">
                            <CheckIcon width={20} height={20} />
                        </DropdownMenu.ItemIndicator>
                    </DropdownMenu.CheckboxItem>

                    <DropdownMenu.CheckboxItem
                        className="flex flex-row items-center gap-x-3 px-2 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm"
                        checked={oneYearChecked}
                        onCheckedChange={setOneYearChecked}
                    >
                        Past 1 Year
                        <DropdownMenu.ItemIndicator className="DropdownMenuItemIndicator">
                            <CheckIcon width={20} height={20} />
                        </DropdownMenu.ItemIndicator>
                    </DropdownMenu.CheckboxItem>

                    <DropdownMenu.CheckboxItem
                        className="flex flex-row items-center gap-x-3 px-2 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm"
                        checked={fiveYearChecked}
                        onCheckedChange={setFiveYearChecked}
                    >
                        Past 5 Years
                        <DropdownMenu.ItemIndicator className="DropdownMenuItemIndicator">
                            <CheckIcon width={20} height={20} />
                        </DropdownMenu.ItemIndicator>
                    </DropdownMenu.CheckboxItem>


                    <DropdownMenu.CheckboxItem
                        className="flex flex-row items-center gap-x-3 px-2 py-1 hover:bg-[#F6F6F6] focus:outline-[1.5px] focus:outline-[#DFDFDF] rounded-sm"
                        checked={tenYearChecked}
                        onCheckedChange={setTenYearChecked}
                    >
                        Past 10 Years
                        <DropdownMenu.ItemIndicator className="DropdownMenuItemIndicator">
                            <CheckIcon width={20} height={20} />
                        </DropdownMenu.ItemIndicator>
                    </DropdownMenu.CheckboxItem>


                </DropdownMenu.Content>
            </DropdownMenu.Portal>
        </DropdownMenu.Root>

	);
};
