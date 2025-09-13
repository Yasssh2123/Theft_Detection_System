from ultralytics import YOLO
import openvino as ov

def optimize_yolo_model(model_path, output_path):
    """Convert and optimize YOLO model for OpenVINO with quantization"""
    
    # Load YOLO model
    model = YOLO(model_path)
    
    # Export to OpenVINO with INT8 quantization
    model.export(
        format='openvino',
        int8=True,  # Enable INT8 quantization for faster CPU inference
        dynamic=False,  # Static shapes for better optimization
        simplify=True,  # Simplify model structure
        workspace=4,  # Optimize memory usage
        half=False,
        data=r"C:\Users\yashc\Downloads\nuebAIstic\FYP-Shoplift.v21i.yolov11\data.yaml"  # Disable FP16 for CPU
    )
    
    print(f"Optimized model saved to: {output_path}")

def further_optimize_openvino(model_path):
    """Additional OpenVINO optimizations"""
    core = ov.Core()
    
    # Load model
    model = core.read_model(model_path)
    
    # Compile with CPU optimizations
    compiled_model = core.compile_model(
        model, 
        device_name="CPU",
        config={
            "CPU_THREADS_NUM": "0",  # Use all available cores
            "CPU_BIND_THREAD": "YES",  # Bind threads to cores
            "CPU_THROUGHPUT_STREAMS": "1",  # Optimize for latency
            "INFERENCE_PRECISION_HINT": "int8"  # Use INT8 precision
        }
    )
    
    return compiled_model

if __name__ == "__main__":
    # Optimize your model
    model_path = r"C:\Users\yashc\Downloads\nuebAIstic\Theft_Detection_e200_smallModel_FYP_Dataset\Theft_Detection_e200_smallModel_FYP_Dataset\weights\best.pt"  # Your original model
    optimize_yolo_model(model_path, "best_optimized_openvino_model")