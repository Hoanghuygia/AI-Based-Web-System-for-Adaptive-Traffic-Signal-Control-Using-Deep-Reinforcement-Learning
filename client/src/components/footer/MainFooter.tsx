import AcademicInformation from "./AcademicInformation";
import ResearchResourcesContact from "./ResearchResourcesContact";
import TechNologyQuickLink from "./TechnologyQuickLink";
import ProjectInformation from "./ProjectInformation";
import CopyRight from "./Copyright";

const MainFooter = () => {
    const techBadges = [
        "SUMO",
        "Python",
        "PyTorch",
        "MARL",
        "PPO",
        "LSTM",
        "FastAPI",
        "React",
        "Tailwind",
        "OSM",
    ];

    return (
        <footer className="bg-gray-50 border-t border-gray-200 mt-8">
            <div className="max-w-7xl mx-auto px-6 py-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {/* PROJECT INFORMATION */}
                    <ProjectInformation />

                    {/* ACADEMIC INFORMATION */}
                    <AcademicInformation />

                    {/* TECHNOLOGIES & QUICK LINKS */}
                    <TechNologyQuickLink
                        techBadges={techBadges}
                    />

                    {/* RESEARCH, RESOURCES & CONTACT */}
                    <ResearchResourcesContact />
                </div>

                {/* Bottom Copyright */}
                <CopyRight />
            </div>
        </footer>
    );
};

export default MainFooter;
