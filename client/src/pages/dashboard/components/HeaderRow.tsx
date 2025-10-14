type HeaderRowProps = {};

const HeaderRow: React.FC<HeaderRowProps> = ({}) => {
    return (
        <div
            className="w-full flex flex-row items-center
        bg-gray-200 rounded-t-lg px-6 py-3 text-gray-600 font-semibold text-sm uppercase tracking-wider shadow-sm"
        >
            <p className="flex-[3] text-left">
                Junction Name
            </p>
            <p className="flex-[2] text-center">Status</p>
            <p className="flex-[1] text-left">
                Last Update
            </p>
        </div>
    );
};

export default HeaderRow;
