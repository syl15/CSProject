import React from 'react'
import { Tooltip } from "radix-ui";
import { PlusIcon, InfoCircledIcon } from "@radix-ui/react-icons";


export default function ToolTip({paragraph}) {
  return (
    <Tooltip.Provider>
        <Tooltip.Root>
            <Tooltip.Trigger asChild>
                <InfoCircledIcon width="20px" height="20px"/>
            </Tooltip.Trigger>
            <Tooltip.Portal>
                <Tooltip.Content className="max-w-50 bg-[#ECECEC] rounded-md text-xs p-3" sideOffset={5}>
                    {paragraph}
                    <Tooltip.Arrow className="fill-[#ECECEC]" />
                </Tooltip.Content>
            </Tooltip.Portal>
        </Tooltip.Root>
    </Tooltip.Provider>
  );
}
