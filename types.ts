export interface CroppedSegment {
  id: number;
  dataUrl: string;
  row: number;
  col: number;
}

export interface ImageDimensions {
  width: number;
  height: number;
}

export interface GridConfig {
  rows: number;
  cols: number;
}
