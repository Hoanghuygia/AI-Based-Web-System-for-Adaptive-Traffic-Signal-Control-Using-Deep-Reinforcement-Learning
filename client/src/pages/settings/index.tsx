import AccountSettings from "./components/AccountSettings";
import NotificationSettings from "./components/NotificationSettings";
import SystemPreferences from "./components/SystemPreferences";
import DisplaySettings from "./components/DisplaySettings";
import SecuritySettings from "./components/SecuritySettings";
import DataSettings from "./components/DataSettings";
import APISettings from "./components/APISettings";
import { useState } from "react";
import { Button } from "antd";
import {
    EditOutlined,
    SaveOutlined,
} from "@ant-design/icons";

export default function Settings() {
    console.log("Render Settings");

    const [isEdit, setIsEdit] = useState(false);
    const [saveMessage, setSaveMessage] = useState("");

    const handleSave = () => {
        setTimeout(() => {
            setSaveMessage("Settings saved successfully!");
            setIsEdit(false);
            setTimeout(() => setSaveMessage(""), 3000);
        }, 1000);
    };

    const handleCancel = () => {
        setIsEdit(false);
        setSaveMessage("");
    };

    return (
        <div
            id="setting-page"
            className="bg-white relative"
        >
            {saveMessage && (
                <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
                    {saveMessage}
                </div>
            )}

            {/* Account settings */}
            <AccountSettings disabled={!isEdit} />
            <NotificationSettings disabled={!isEdit} />
            <SystemPreferences disabled={!isEdit} />
            <DisplaySettings disabled={!isEdit} />
            <SecuritySettings disabled={!isEdit} />
            <DataSettings disabled={!isEdit} />
            <APISettings disabled={!isEdit} />

            {/* Bottom action buttons */}
            <div className="flex justify-end mt-6 gap-2">
                {isEdit ? (
                    <>
                        <Button
                            onClick={handleCancel}
                            type="primary"
                            className="!bg-white hover:!bg-gray-200 !border-gray-300 h-12 w-24 !text-black"
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={handleSave}
                            type="primary"
                            className="!bg-purple-400 hover:!bg-purple-500 !border-purple-400 h-12"
                        >
                            <SaveOutlined />
                            Save Changes
                        </Button>
                    </>
                ) : (
                    <>
                        <Button
                            onClick={() => setIsEdit(true)}
                            type="primary"
                            size="large"
                            className="!bg-purple-400 hover:!bg-purple-500 !border-purple-400 h-12"
                        >
                            <EditOutlined />
                            Edit Settings
                        </Button>
                    </>
                )}
            </div>
        </div>
    );
}
