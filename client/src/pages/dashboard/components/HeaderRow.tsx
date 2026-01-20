import { useTranslation } from "react-i18next";

type HeaderRowProps = {};

const HeaderRow: React.FC<HeaderRowProps> = ({}) => {
    const { t } = useTranslation();
    
    return (
        <div
            className="w-full flex flex-row items-center
        bg-gray-200 rounded-t-lg px-6 py-3 text-gray-600 font-semibold text-sm uppercase tracking-wider shadow-sm"
        >
            <p className="flex-[3] text-left">
                {t("dashboard.table.header.junctionName")}
            </p>
            <p className="flex-[2] text-center">{t("dashboard.table.header.status")}</p>
            <p className="flex-[1] text-left">
                {t("dashboard.table.header.lastUpdate")}
            </p>
        </div>
    );
};

export default HeaderRow;
