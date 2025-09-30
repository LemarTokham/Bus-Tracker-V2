import React from "react"

type BusLineSelectorProps = {
    arrivaLines: string[]
    stageCoachLines: string[]
    onBusClick: (busLine: string, busCompany: string) => void
}

const BusLineSelector =  ({
    arrivaLines,
    stageCoachLines,
    onBusClick,
} : BusLineSelectorProps) => {
    return (
        <div>
            {arrivaLines.length > 0 &&  (
                <div>
                    <h3>Arriva Buses</h3>
                    <ul>
                        {arrivaLines.map((line) => (
                            <li key={`arriva-${line}`}>
                                <button onClick={() => onBusClick(line, "arriva")}>
                                    {line}
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            {stageCoachLines.length > 0 && (
                <div>
                    <h3>Stagecoach Buses</h3>
                    <ul>
                        {stageCoachLines.map((line) => (
                            <li key={`stagecoach-${line}`}>
                                <button onClick={()=> onBusClick(line, "stagecoach")}>
                                    {line}
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    )
}

export default BusLineSelector