"""
Process an image using different effects
"""
import cv2 as cv
import numpy as np


class ImgProcessor:
    """Apply different effects to an image"""

    def __init__(self, img: bytes):
        """Init

        Args:
            - img (bytes): Image to be processed
        """

        self.__src_img = self.__img_decode(img)
        self.__dst_img = img

    def __img_decode(self, img: bytes) -> np.ndarray:
        """Convert an image into numpy array compatible with OpenCV

        Args:
            - img (bytes): Image to be converted

        Returns:
            - numpy array: Image converted to an OpenCV format
        """

        img_np = np.frombuffer(img, np.uint8)
        return cv.imdecode(img_np, cv.IMREAD_COLOR)

    def __img_encode(self, img: np.ndarray, format: str = "jpg") -> np.ndarray:
        """Convert an OpenCV numpy array into an image
        Supported formats are:
            Windows bitmaps - *.bmp, *.dib
            JPEG files - *.jpeg, *.jpg, *.jpe
            JPEG 2000 files - *.jp2
            Portable Network Graphics - *.png
            WebP - *.webp
            Portable image format - *.pbm, *.pgm, *.ppm *.pxm, *.pnm
            PFM files - *.pfm
            Sun rasters - *.sr, *.ras
            TIFF files - *.tiff, *.tif
            OpenEXR Image files - *.exr
            Radiance HDR - *.hdr, *.pic
            Raster and Vector geospatial data supported by GDAL

        Args:
            - img (np.ndarray): Image to be converted
            - format (str): Output format for the image. Default: jpg

        Returns:
            - numpy array: Image converted to an array of bytes
        """

        return cv.imencode("." + format, img)[1]

    def __store_result(func):
        """Decorator to keep a byte copy of the customized image"""

        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.__dst_img = self.__img_encode(img=result)
            return result

        return wrapper

    def src_image(self) -> np.ndarray:
        """Return the original image"""

        return self.__src_img

    def dst_image(self) -> np.ndarray:
        """Return the customized image"""

        return self.__dst_img

    @__store_result
    def rotate(self, degrees: int = 90, clockwise: bool = True) -> np.ndarray:
        """Rotate an image 90 or 180 degrees

        Args:
            - degrees (int): Degrees of rotation.
                Any value but 90 will default into 180 degrees. Default: 90
            - clockwise (bool): When degrees=90, determines if the rotation is clockwise or not

        Returns:
            - numpy array: Image rotated as an OpenCV numpy array
        """

        img = self.__src_img
        if degrees == 90:
            return (
                cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
                if clockwise
                else cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
            )
        return cv.rotate(img, cv.ROTATE_180)

    @__store_result
    def grayscale(self) -> np.ndarray:
        """Convert an image to grayscale

        Returns:
            - numpy array: Image in grayscale as an OpenCV numpy array
        """

        img = self.__src_img
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    @__store_result
    def negative(self) -> np.ndarray:
        """Covert an image to its negative

        Returns:
            - numpy array: Negative of the image as an OpenCV numpy array
        """

        img = self.__src_img
        return cv.bitwise_not(img)

    @__store_result
    def flip(self, axis: str = "b") -> np.ndarray:
        """Flip an image over its axis

        Args:
            - axis (str): Axis to rotate the image. Possible values are
                X (x axis), Y (y axis), B (both axis). Any other value
                will default to "b". Default: b

        Returns:
            - numpy array: Image fliped as an OpenCV numpy array
        """

        img = self.__src_img
        if axis.lower() == "x":
            return cv.flip(img, 0)
        if axis.lower() == "y":
            return cv.flip(img, 1)
        return cv.flip(img, -1)

    @__store_result
    def sharp(self) -> np.ndarray:
        """Sharp effect over an image

        Returns:
            - numpy array: Image sharped as an OpenCV numpy array
        """

        img = self.__src_img
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        return cv.filter2D(img, -1, kernel)

    @__store_result
    def sepia(self) -> np.ndarray:
        """Sepia effect over an image

        Returns:
            - numpy array: Image in sepia as an OpenCV numpy array
        """

        img_rgb = cv.cvtColor(self.__src_img, cv.COLOR_BGR2RGB)
        kernel = np.array(
            [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
        )
        return cv.transform(img_rgb, kernel)

    @__store_result
    def blur(self, factor: int = 35) -> np.ndarray:
        """Blur effect over an image

        Args:
            - factor (int): Blur intensity. Positive odd numbers only. Default: 35

        Returns:
            - numpy array: Image blured as an OpenCV numpy array
        """

        img = self.__src_img
        if not factor % 2:
            factor += 1
        return cv.GaussianBlur(img, (factor, factor), 0)

    @__store_result
    def emboss(self) -> np.ndarray:
        """Emboss effect over an image

        Returns:
            - numpy array: Image with emboss effect as an OpenCV numpy array
        """

        img = self.__src_img
        kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])
        return cv.filter2D(img, -1, kernel)

    @__store_result
    def scale(self, factor: float = 1) -> np.ndarray:
        """Scale an image using a factor

        Args:
            - factor (float): Scale factor. Postive float number. Default: 1

        Returns:
            - numpy array: Scaled image as an OpenCV numpy array
        """

        img = self.__src_img
        height, width = img.shape[:2]
        new_height = int(height * factor)
        new_width = int(width * factor)
        return cv.resize(img, (new_width, new_height))

    @__store_result
    def noise(self, factor: float = 0.2) -> np.ndarray:
        """Add noise to an image

        Args:
            - factor (float): Amount of noise injected. Default: 0.2

        Returns:
            - numpy array: Image with noise injected as an OpenCV numpy array
        """

        img = self.__src_img
        noise = np.zeros(img.shape)
        cv.randu(noise, 0, 256)
        return img + np.array(factor * noise)

    @__store_result
    def laplacian(self, factor: int = 5) -> np.ndarray:
        """Laplacian effect over an image

        Args:
            - factor (int): Effect intensity. Positive odd numbers only. Default: 5

        Returns:
            - numpy array: Image with laplacian effect as an OpenCV numpy array
        """

        img = self.__src_img
        if not factor % 2:
            factor += 1
        return cv.Laplacian(img, cv.CV_64F, ksize=factor)

    @__store_result
    def sobel(self, factor: int = 3, horizontal=True) -> np.ndarray:
        """Sobel effect over an image

        Args:
            - factor (int): Effect intensity. Positive odd numbers only. Default: 3
            - horizontal (bool): If True, effect's direcion is horizontal.
                Otherwise direction is vertical. Default: True

        Returns:
            - numpy array: Image with sobel effect as an OpenCV numpy array
        """

        img = self.__src_img
        if not factor % 2:
            factor += 1
        dx, dy = (1, 0) if horizontal else (0, 1)
        return cv.Sobel(img, cv.CV_64F, dx, dy, ksize=factor)


if __name__ == "__main__":

    with open("city.jpg", "rb") as f:
        image = f.read()
    test = ImgProcessor(image)

    with open("test.jpg", "wb") as f:
        test.sepia()
        test.negative()
        f.write(test.dst_image())
