import asyncio
from io import BytesIO
import os.path

from fastapi import FastAPI, File, UploadFile, HTTPException, Path, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from PIL import Image, ImageOps
import tiffslide

from scripts.tile_post_process import PostProcess

current_directory = os.path.dirname(os.path.abspath(__file__))

script_globals = {'ImageOps': ImageOps}  # Inject ImageOps into the globals
script_locals = {}

def load_script():
    global script_globals, script_locals
    script_locals.clear()  # Clear the local namespace before reloading the script
    script_path = os.path.join(current_directory, 'scripts', 'dynamic_scripts.py')
    if os.path.exists(script_path):
        with open(script_path, 'r') as script_file:
            script_content = script_file.read()
            try:
                print(f"Executing script:\n{script_content}")  # Log the script content
                exec(script_content, script_globals, script_locals)
                print("Script executed successfully")
            except Exception as e:
                print(f"Error executing script: {str(e)}")
                raise  # Re-raise the exception for more visibility
    else:
        print(f"Script file {script_path} does not exist")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_EXTENSIONS = {'svs', 'tif', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

slide = None


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global slide
    if not file:
        raise HTTPException(status_code=400, detail="No file part")
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")
    if file and allowed_file(file.filename):
        try:
            content = await file.read()
            file_content = BytesIO(content)
            
            slide = tiffslide.TiffSlide(file_content)
            
            return JSONResponse(content={
                'message': 'File uploaded and processed successfully',
                'filename': file.filename,
                'dimensions': slide.level_dimensions
            }, status_code=200)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error processing file: {str(e)}') from e
    else:
        raise HTTPException(status_code=400, detail="File type not allowed")


@app.get("/load/{filename:path}")
async def load_slide(filename: str = Path(...)):
    global slide
    
    if slide is not None:
        try:
            return JSONResponse(content={
                'message': 'Slide loaded successfully',
                'dimensions': slide.level_dimensions
            }, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'Error loading slide: {str(e)}') from e
    else:
        raise HTTPException(status_code=404, detail="No slide loaded")


@app.get("/slide/{level:int}/{col:int}_{row:int}.jpeg")
async def get_tile(level: int, col: int, row: int):
    global slide
    if slide is None:
        raise HTTPException(status_code=400, detail="No slide loaded")
    
    try:
        size = 512
        max_svs_level = len(slide.level_dimensions)
        dzi_level = level
        svs_level = max_svs_level - dzi_level - 1

        adjust_ratio = 1
        if svs_level >= len(slide.level_dimensions):
            raise HTTPException(status_code=404, detail="Invalid level")
        elif svs_level < 0:
            level_overflow = abs(svs_level)
            adjust_ratio = 2**(dzi_level - level_overflow * 2)
            svs_level = 0
        else:
            adjust_ratio = 2**dzi_level
        zoom_ratio = slide.level_dimensions[0][0] / slide.level_dimensions[svs_level][0]
        
        x = int(col * size * zoom_ratio * adjust_ratio)
        y = int(row * size * zoom_ratio * adjust_ratio)
        img = slide.read_region((x, y), svs_level, (size * adjust_ratio, size * adjust_ratio))
        img = img.resize((size, size))
        
        post_processor = PostProcess(img, svs_level, app)
        post_processor.run()
        img = post_processor.img

        try:
            load_script()  # Check for updates and load the script
            print(111111111111111)
            if 'process_tile' in script_locals:
                print(22222222222)
                print(script_locals)
                img = script_locals['process_tile'](img)
        except Exception as e:
            print("Error inside 'process_tile':", e)
            return JSONResponse(content={'error': f"Error inside 'process_tile': {str(e)}"}, status_code=500)


        img_io = BytesIO()
        img.convert('RGB').save(img_io, 'JPEG', quality=70)
        img_io.seek(0)

        return StreamingResponse(img_io, media_type='image/jpeg')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error processing tile: {str(e)}') from e


@app.post("/update-script")
async def update_script(request: Request):
    req = await request.json()
    script_content = req.get('script')
    if not script_content:
        raise HTTPException(status_code=400, detail="No script content provided")
    
    script_path = os.path.join(current_directory, 'scripts', 'dynamic_scripts.py')
    with open(script_path, 'w') as script_file:
        script_file.write(script_content)
    
    return JSONResponse(content={'message': 'Script updated successfully'}, status_code=200)


progress = 0

@app.post("/run-preprocess")
async def run_preprocess(request: Request):
    global progress
    progress = 0
    req = await request.json()
    params = req.get('params')
    return JSONResponse(content={'message': 'Preprocess started'}, status_code=200)


@app.get("/get-progress")
async def get_progress():
    global progress
    if progress < 100:
        progress += 10
        await asyncio.sleep(0.2)
    return JSONResponse(content={'progress': progress}, status_code=200)

@app.get("/get-result")
async def get_result():
    global progress
    if progress >= 100:
        return JSONResponse(content={'message': 'Run preprocess finished successfully', "number_of_nuclei": "50000"}, status_code=200)
    else:
        return JSONResponse(content={'message': 'Processing not complete yet'}, status_code=202)

