import cv2 as cv
from imutils import contours
import pytesseract
import sudoku
import constraint_propagation

class SudokuImageProcessor:
    def __init__(self, image):
        '''Initialize with image of sudoku board
        On initialization, estimates acceptable size of sudoku cells (cell_min and cell_max) based on area of image divided by 81 (number of sudoku cells) and scalar
        '''
        self.image = image
        self.cell_min = (image.shape[0] * image.shape[1]) / 81 * 0.5
        self.cell_max = (image.shape[0] * image.shape[1]) / 81 * 1.5

    def convert_to_array(self):
        '''Convert sudoku image into array representation e.g., [][] with sudoku cell values or zero for empty spaces
        Params: None
        Returns: sudoku board [][]
        '''
        inv_binary_image = self.preprocess()
        cnts = self.find_sudoku_cells(inv_binary_image)
        return self.extract_cell_values(cv.bitwise_not(inv_binary_image), cnts)

    def preprocess(self):
        '''Preprocess sudoku image to facilitate contour detection and OCR
        Converts to grayscale, blurs image to reduce noise, and uses adaptive thresholding to convert to binary image ()
        Params: None
        Returns: binary image [][]
        '''
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        blur = cv.medianBlur(gray, 5)
        return cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, 11)
    
    def find_sudoku_cells(self, binary_image):
        '''Takes inverse binary image and finds sudoku cells, returns contours of cells sorted from from left-to-right and top-to-bottom
        Before identifying contours, uses morhphological close to ensure sudoku grid is complete.
        Binary image must be inverted, i.e., black background and white objects.
        Params: binary image [][]
        Returns: [][] of contours
        '''
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
        close = cv.morphologyEx(binary_image, cv.MORPH_CLOSE, kernel, iterations=3)
        cnts = cv.findContours(close, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)[0]
        return self.sort_sudoku_cell_contours(cnts)
    
    def sort_sudoku_cell_contours(self, cnts):
        '''Takes contours and tries to identify the contours associated with sudoku cells and then sorts and returns the associated contours
        Cell contours are sorted left-to-right and top-to-bottom, e.g., the top left sudoku cell is in position [0][0] while the bottom right is in [8][8]
        To identify sudoku cells, algorithm ignores contours below a min area and above a max area, determined by dividing the image 81 cells and adjusting by a scaler (see __init__)
        Params: contours (vector of points)
        Returns: [][] sorted array of contours associated with sudoku cells
        '''
        row = []
        board = []
        cnts = contours.sort_contours(cnts, method = 'top-to-bottom')[0]
        for c in cnts:
            area = cv.contourArea(c)
            if area < self.cell_min or area > self.cell_max:
                continue

            row.append(c)
            if len(row) == 9:
                sorted = contours.sort_contours(row, method = 'left-to-right')[0]
                board.append(sorted)
                row = []
        return board

    def extract_cell_values(self, binary_image, cnts):
        '''Iterates through sorted contours of sudoku board and returns a 2D array with sudoku values from binary image
        Contours must be sorted from left-to-right and top-to-bottom, binary image works best with black text against white background
        Params: binary image [][], [][] contours associated with sudoku board cells
        Returns: [][] with sudoku cell values (zero for empty)
        '''
        res = [[0 for _ in range(9)] for _ in range(9)]
        for i, r in enumerate(cnts):
            for j, c in enumerate(r):
                x, y, w, h = cv.boundingRect(c)
                cv.rectangle(binary_image, (x, y), (x + w, y + h), (256, 256, 256), 7)
                value = pytesseract.image_to_string(binary_image[y:y + h, x:x + w], lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=123456789').rstrip()
                if value == '': continue
                res[i][j] = int(value)
        return res
