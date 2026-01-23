import QuickLink from "./QuickLink";

type TechnologyQuickLinkProps = {
    techBadges: string[];
};

export default function TechNologyQuickLink({ techBadges }: TechnologyQuickLinkProps) {
    return (
        <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4">
                Technologies
            </h3>
            <div className="flex flex-wrap gap-2 mb-6">
                {techBadges.map((tech) => (
                    <span
                        key={tech}
                        className="px-2.5 py-1 bg-white border border-gray-300 rounded text-xs font-medium text-gray-700"
                    >
                        {tech}
                    </span>
                ))}
            </div>

            <QuickLink />
        </div>
    );
}
