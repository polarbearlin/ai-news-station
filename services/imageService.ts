import { CroppedSegment } from '../types';
import { GoogleGenAI, Type } from "@google/genai";

/**
 * Loads an image from a source string (URL or DataURL).
 */
export const loadImage = (src: string): Promise<HTMLImageElement> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => resolve(img);
    img.onerror = (e) => reject(new Error('Failed to load image'));
    img.src = src;
  });
};

const fileToGenerativePart = async (file: File) => {
  const base64EncodedDataPromise = new Promise<string>((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve((reader.result as string).split(',')[1]);
    reader.readAsDataURL(file);
  });
  return {
    inlineData: { data: await base64EncodedDataPromise, mimeType: file.type },
  };
};

/**
 * Uses Gemini to detect the grid structure of an uploaded image.
 */
export const detectGridStructure = async (file: File): Promise<{ rows: number; cols: number }> => {
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
    const imagePart = await fileToGenerativePart(file);

    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: {
        parts: [
          imagePart,
          { 
            text: "Analyze this image. It appears to be a grid, sprite sheet, or collage containing multiple items arranged in rows and columns. Count the precise number of rows and columns. If it is a single image without a clear grid, return rows: 3, cols: 3 as a default. Return JSON." 
          }
        ]
      },
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            rows: { type: Type.INTEGER, description: "Number of rows in the grid" },
            cols: { type: Type.INTEGER, description: "Number of columns in the grid" }
          },
          required: ["rows", "cols"]
        }
      }
    });

    const result = JSON.parse(response.text || "{}");
    return {
      rows: Math.max(1, result.rows || 3),
      cols: Math.max(1, result.cols || 3)
    };
  } catch (error) {
    console.warn("Grid detection failed, defaulting to 3x3", error);
    return { rows: 3, cols: 3 };
  }
};

/**
 * Splits an image into a grid based on specified rows and cols.
 */
export const splitImageIntoGrid = async (imageSrc: string, rows: number, cols: number): Promise<CroppedSegment[]> => {
  const img = await loadImage(imageSrc);
  const segments: CroppedSegment[] = [];
  
  // Calculate segment dimensions using floating point to be precise
  const segmentWidth = img.width / cols;
  const segmentHeight = img.height / rows;

  for (let row = 0; row < rows; row++) {
    for (let col = 0; col < cols; col++) {
      const canvas = document.createElement('canvas');
      
      canvas.width = segmentWidth;
      canvas.height = segmentHeight;
      
      const ctx = canvas.getContext('2d');
      if (!ctx) {
        throw new Error('Could not get canvas context');
      }

      // Draw the specific portion of the source image onto the canvas
      ctx.drawImage(
        img,
        col * segmentWidth, // Source X
        row * segmentHeight, // Source Y
        segmentWidth, // Source Width
        segmentHeight, // Source Height
        0, // Dest X
        0, // Dest Y
        canvas.width, // Dest Width
        canvas.height // Dest Height
      );

      segments.push({
        id: row * cols + col,
        dataUrl: canvas.toDataURL('image/png'),
        row,
        col
      });
    }
  }

  return segments;
};

/**
 * Triggers a download for a specific Data URL.
 */
export const downloadImage = (dataUrl: string, filename: string) => {
  const link = document.createElement('a');
  link.href = dataUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};
