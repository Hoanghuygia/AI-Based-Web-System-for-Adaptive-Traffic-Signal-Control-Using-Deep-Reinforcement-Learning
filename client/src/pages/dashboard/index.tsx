import { Button, Dropdown, Input } from "antd";
import { SearchOutlined, FilterOutlined } from "@ant-design/icons";
import HeaderRow from "./components/HeaderRow";
import JunctionCard from "./components/JunctionCard";

export default function Dashboard() {
    console.log("Render Dashboard");
    const handleClick = (id: string) => {
        console.log("Clicked junction ID:", id);
    };

    const items = [
        {
            key: "1",
            label: "All",
        },
        {
            key: "2",
            label: "Heavy Traffic",
        },
        {
            key: "3",
            label: "Moderate Traffic",
        },
        {
            key: "4",
            label: "Light Traffic",
        },
    ];

    type TrafficStatus = "low" | "medium" | "high";

    const junctionData: {
        id: string;
        name: string;
        lat: number;
        lng: number;
        status: TrafficStatus;
        lastUpdated: string;
        congestionLevel: number;
        location: string;
    }[] = [
        {
            id: "411926580",
            name: "Hai Ba Trung - Nguyen Thi Minh Khai",
            lat: 10.782879,
            lng: 106.698107,
            status: "high",
            lastUpdated: "5 minutes ago",
            congestionLevel: 85,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411925946",
            name: "Pham Ngoc Thach - Nguyen Thi Minh Khai",
            lat: 10.781696,
            lng: 106.696943,
            status: "medium",
            lastUpdated: "2 minutes ago",
            congestionLevel: 45,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926604",
            name: "Pasteur - Nguyen Thi Minh Khai",
            lat: 10.780516,
            lng: 106.695852,
            status: "low",
            lastUpdated: "1 minute ago",
            congestionLevel: 15,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "2664205599",
            name: "Nam Ky Khoi Nghia - Nguyen Thi Minh Khai",
            lat: 10.779559,
            lng: 106.694981,
            status: "high",
            lastUpdated: "3 minutes ago",
            congestionLevel: 90,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926212",
            name: "Nam Ky Khoi Nghia - Vo Van Tan",
            lat: 10.780477,
            lng: 106.693959,
            status: "medium",
            lastUpdated: "7 minutes ago",
            congestionLevel: 50,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411925942",
            name: "Pasteur - Vo Van Tan",
            lat: 10.781432,
            lng: 106.6948,
            status: "low",
            lastUpdated: "10 minutes ago",
            congestionLevel: 20,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926599",
            name: "Ho Con Rua",
            lat: 10.782695,
            lng: 106.695875,
            status: "medium",
            lastUpdated: "4 minutes ago",
            congestionLevel: 60,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926578",
            name: "Hai Ba Trung - Tran Cao Van",
            lat: 10.783801,
            lng: 106.697048,
            status: "high",
            lastUpdated: "6 minutes ago",
            congestionLevel: 80,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926523",
            name: "Hai Ba Trung - Nguyen Dinh Chieu",
            lat: 10.784677,
            lng: 106.695944,
            status: "medium",
            lastUpdated: "1 minute ago",
            congestionLevel: 35,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926597",
            name: "Pham Ngoc Thach - Nguyen Dinh Chieu",
            lat: 10.783561,
            lng: 106.694855,
            status: "low",
            lastUpdated: "8 minutes ago",
            congestionLevel: 25,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926554",
            name: "Pasteur - Nguyen Dinh Chieu",
            lat: 10.782421,
            lng: 106.693784,
            status: "high",
            lastUpdated: "3 minutes ago",
            congestionLevel: 75,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926164",
            name: "Nam Ky Khoi Nghia - Nguyen Dinh Chieu",
            lat: 10.781454,
            lng: 106.692907,
            status: "medium",
            lastUpdated: "9 minutes ago",
            congestionLevel: 55,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926532",
            name: "Nam Ky Khoi Nghia - Dien Bien Phu",
            lat: 10.783504,
            lng: 106.690758,
            status: "high",
            lastUpdated: "2 minutes ago",
            congestionLevel: 92,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926559",
            name: "Pasteur - Dien Bien Phu",
            lat: 10.784368,
            lng: 106.691692,
            status: "medium",
            lastUpdated: "5 minutes ago",
            congestionLevel: 40,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926419",
            name: "Pham Ngoc Thach - Dien Bien Phu",
            lat: 10.78551,
            lng: 106.692774,
            status: "low",
            lastUpdated: "1 minute ago",
            congestionLevel: 10,
            location: "District 3, Ho Chi Minh City",
        },
        {
            id: "411926477",
            name: "Hai Ba Trung - Dien Bien Phu",
            lat: 10.786472,
            lng: 106.693728,
            status: "high",
            lastUpdated: "4 minutes ago",
            congestionLevel: 88,
            location: "District 3, Ho Chi Minh City",
        },
    ];

    return (
        <div className="flex flex-col justify-start items-center gap-y-5 p-4">
            <div className="w-full flex flex-col justify-center items-start">
                <h1 className="text-2xl font-bold mb-4">
                    Traffic Junction List
                </h1>
                <p>
                    Monitor and manage traffic congestion at
                    various junctions in District 3, Ho Chi
                    Minh City
                </p>
            </div>
            <div
                id="filter-bar"
                className="w-full flex flex-row justify-start items-center bg-gray-200 p-4 rounded-md"
            >
                <div className="relative flex-1">
                    <SearchOutlined className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 z-10" />
                    <Input
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2
                        focus:ring-purple-500 focus:border-transparent  hover:!border-purple-500 hover:!text-purple-500 transition duration-300"
                        placeholder="Search junctions..."
                    />
                </div>

                <Dropdown
                    menu={{ items }}
                    overlayClassName="custom-dropdown-search-bar"
                    placement="bottomLeft"
                    trigger={["click"]}
                >
                    <Button
                        icon={<FilterOutlined />}
                        className="ml-4 h-10 bg-white rounded-md 
                    hover:!border-purple-500 hover:!text-purple-500 
                    transition duration-300"
                    >
                        Filter By Status
                    </Button>
                </Dropdown>
            </div>
            <div className="w-full flex flex-col justify-start items-center">
                <HeaderRow />
                <div className="w-full mx-auto mt-4">
                    {junctionData.map((junction) => (
                        <JunctionCard
                            key={junction.id}
                            junction={junction}
                            onClick={handleClick}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}
