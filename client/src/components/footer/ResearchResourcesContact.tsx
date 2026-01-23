import { Github, Mail, Linkedin } from "lucide-react";

export default function ResearchResourcesContact() {
    return (
        <div>
            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
                Research
            </h3>
            <ul className="space-y-2 text-sm mb-6">
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors inline-flex items-center"
                    >
                        Paper References
                        <svg
                            className="w-3 h-3 ml-1"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors inline-flex items-center"
                    >
                        Algorithm Explanation
                        <svg
                            className="w-3 h-3 ml-1"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </a>
                </li>
            </ul>

            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
                Resources
            </h3>
            <ul className="space-y-2 text-sm mb-6">
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors inline-flex items-center"
                    >
                        Dataset Description
                        <svg
                            className="w-3 h-3 ml-1"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors inline-flex items-center"
                    >
                        Experiment Setup
                        <svg
                            className="w-3 h-3 ml-1"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </a>
                </li>
                <li>
                    <a
                        href="#"
                        className="text-gray-600 hover:text-gray-900 transition-colors inline-flex items-center"
                    >
                        Evaluation Metrics
                        <svg
                            className="w-3 h-3 ml-1"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </a>
                </li>
            </ul>

            <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-3">
                Contact & Code
            </h3>
            <div className="flex gap-3">
                <a
                    href="#"
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                    aria-label="GitHub"
                >
                    <Github className="w-5 h-5" />
                </a>
                <a
                    href="#"
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                    aria-label="Email"
                >
                    <Mail className="w-5 h-5" />
                </a>
                <a
                    href="#"
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                    aria-label="LinkedIn"
                >
                    <Linkedin className="w-5 h-5" />
                </a>
            </div>
        </div>
    );
}
