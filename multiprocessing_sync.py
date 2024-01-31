import cv2
import multiprocessing as mp
import time
  
def camera(number):
    vid = cv2.VideoCapture(number) 

    width= int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'output_{number}.mp4', fourcc, 20.0, (width, height))    
    
    while True:
        ret, frame = vid.read() 
        cv2.imshow('frame', frame) 
        out.write(frame)
        
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    
        #if stop.value:
        #    break

    vid.release() 
    out.release()

    print(f"Recording {number} stopped...")
    cv2.destroyAllWindows() 

if __name__ == '__main__':
    #stop = mp.Value('i', 0)
    p1 = mp.Process(target=camera, args=(0,))
    p2 = mp.Process(target=camera, args=(1,))
    
    start = time.time()
    p1.start()
    end = time.time()
    print(f"Camera 1 Start Time: {end-start}")

    start = time.time()
    p2.start()
    end = time.time()
    print(f"Camera 2 Start Time: {end-start}")
    
    #while True:
    #    if input("Press 'q' to stop recording: ") == 'q':
    #        stop.value = 1
    #        break
    
    #p1.join()
    #p2.join()

    end = time.time()

    print(f"Recording stopped. Total time taken: {end-start:.2f} seconds.")