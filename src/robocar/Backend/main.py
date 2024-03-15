from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from datetime import datetime
from model import Command
from robocar.motor_control import MotorControl
from robocar.kinetic_system import KineticSystem
from robocar.navigation_system import NavigationSystem

app = FastAPI()

# Instance initialization
motor_control = MotorControl()
kinetic_system = KineticSystem()
navigation_system = NavigationSystem()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/stream/lidar")
async def websocket_lidar(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Replace the following line with actual LiDAR data handling
            await websocket.send_text("Mock LiDAR data")
    except WebSocketDisconnect:
        print("WebSocket disconnected")


@app.websocket("/stream/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await websocket.send_text(f"{current_time} - Mock log message")
            await asyncio.sleep(1)  # Slow down the message rate
    except WebSocketDisconnect:
        print("Client disconnected")


@app.post("/control/kinetic")
async def control_kinetic(command: Command):
    # Implement your kinetic control logic here
    return {"status": "Command received", "command": command.command}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
