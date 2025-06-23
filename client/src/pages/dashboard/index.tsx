import { useState } from "react"

import Header from "./components/Headaer"
import Sidebar from "./components/SideBar"
import FilterBar from "./components/FilterBar"
import JunctionList from "./components/JunctionList"
import junctionData from './data/junctionData';

// // Mock data - replace with your actual data source
// const junctionData = [
//   {
//     id: 1,
//     name: "Nguyen Thi Minh Khai - Vo Thi Sau",
//     status: "high",
//     congestionLevel: 85,
//     lastUpdated: "2 min ago"
//   },
//   {
//     id: 2,
//     name: "Nam Ky Khoi Nghia - Le Van Sy",
//     status: "medium",
//     congestionLevel: 65,
//     lastUpdated: "5 min ago"
//   },
//   {
//     id: 3,
//     name: "Dien Bien Phu - Pasteur",
//     status: "low",
//     congestionLevel: 25,
//     lastUpdated: "1 min ago"
//   },
//   {
//     id: 4,
//     name: "Hai Ba Trung - Tran Quoc Toan",
//     status: "medium",
//     congestionLevel: 55,
//     lastUpdated: "3 min ago"
//   },
//   {
//     id: 5,
//     name: "Cach Mang Thang Tam - Nguyen Dinh Chieu",
//     status: "high",
//     congestionLevel: 90,
//     lastUpdated: "1 min ago"
//   }
// ]

export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const filteredJunctions = junctionData.filter((junction) => {
    const matchesSearch = junction.name.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || junction.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <div className="min-h-screen bg-slate-100">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="flex flex-col md:flex-row">
            <Sidebar />
            <div className="flex-1 p-6">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Traffic Junction List</h2>
                <p className="text-gray-600">
                  Monitor and manage traffic congestion at various junctions in District 3, Ho Chi Minh City
                </p>
              </div>
              <FilterBar
                searchQuery={searchQuery}
                onSearchChange={setSearchQuery}
                onStatusChange={setStatusFilter}
              />
              <JunctionList junctions={filteredJunctions} />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}