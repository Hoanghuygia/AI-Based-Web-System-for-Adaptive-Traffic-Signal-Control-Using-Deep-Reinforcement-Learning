type SingleLegendProps = {
    color: string;
    label: string;
};

export default function SingleLegend({
    color,
    label,
}: SingleLegendProps) {
    return (
        <div className="flex items-center gap-1">
            <div
                className="w-4 h-4 rounded"
                style={{ backgroundColor: color }}
            ></div>
            <span className="text-gray-600">{label}</span>
        </div>
    );
}
