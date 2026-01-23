export default function QuickLink() {
    return (
        <>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
                Quick Links
            </h3>
            <ul className="space-y-2 text-sm">
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors"
                    >
                        Dashboard
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors"
                    >
                        Junction Monitoring
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors"
                    >
                        Analytics & Statistics
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors"
                    >
                        System Architecture
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors"
                    >
                        Documentation
                    </a>
                </li>
            </ul>
        </>
    );
}
