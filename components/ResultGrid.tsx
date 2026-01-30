import React, { useState } from 'react';
import { CroppedSegment, GridConfig } from '../types';
import { Download, RefreshCw, Grid3X3, Check, Settings2 } from 'lucide-react';
import { downloadImage } from '../services/imageService';

interface ResultGridProps {
  originalImage: string;
  segments: CroppedSegment[];
  gridConfig: GridConfig;
  onReset: () => void;
  onGridUpdate: (rows: number, cols: number) => void;
}

const ResultGrid: React.FC<ResultGridProps> = ({ originalImage, segments, gridConfig, onReset, onGridUpdate }) => {
  const [downloadedIds, setDownloadedIds] = useState<Set<number>>(new Set());
  const [downloadingAll, setDownloadingAll] = useState(false);
  const [editingGrid, setEditingGrid] = useState(false);
  const [tempRows, setTempRows] = useState(gridConfig.rows);
  const [tempCols, setTempCols] = useState(gridConfig.cols);

  const handleDownload = (segment: CroppedSegment) => {
    downloadImage(segment.dataUrl, `grid-segment-${segment.row}-${segment.col}.png`);
    setDownloadedIds(prev => new Set(prev).add(segment.id));
    
    setTimeout(() => {
        setDownloadedIds(prev => {
            const next = new Set(prev);
            next.delete(segment.id);
            return next;
        });
    }, 2000);
  };

  const handleDownloadAll = async () => {
    setDownloadingAll(true);
    for (let i = 0; i < segments.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 300));
        handleDownload(segments[i]);
    }
    setDownloadingAll(false);
  };

  const toggleEdit = () => {
    if (editingGrid) {
      // If we were editing, cancel changes
      setTempRows(gridConfig.rows);
      setTempCols(gridConfig.cols);
    } else {
      setTempRows(gridConfig.rows);
      setTempCols(gridConfig.cols);
    }
    setEditingGrid(!editingGrid);
  };

  const applyGridChanges = () => {
    onGridUpdate(tempRows, tempCols);
    setEditingGrid(false);
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
      
      {/* Action Bar */}
      <div className="flex flex-col md:flex-row justify-between items-center bg-slate-900/50 p-4 rounded-xl border border-slate-800 backdrop-blur-md sticky top-4 z-40 shadow-2xl gap-4">
        <div className="flex items-center space-x-4 w-full md:w-auto">
          <div className="p-2 bg-indigo-500/20 rounded-lg shrink-0">
             <Grid3X3 className="w-5 h-5 text-indigo-400" />
          </div>
          
          {!editingGrid ? (
            <div className="flex items-center space-x-4">
              <div>
                <h2 className="text-sm font-semibold text-slate-200">
                  {gridConfig.rows}x{gridConfig.cols} Grid Detected
                </h2>
                <p className="text-xs text-slate-400">{segments.length} segments generated</p>
              </div>
              <button 
                onClick={toggleEdit}
                className="p-1.5 hover:bg-slate-800 rounded-md text-slate-400 hover:text-indigo-400 transition-colors"
                title="Adjust Grid"
              >
                <Settings2 className="w-4 h-4" />
              </button>
            </div>
          ) : (
             <div className="flex items-center space-x-2 animate-in fade-in slide-in-from-left-2">
                <div className="flex items-center space-x-2">
                  <label className="text-xs text-slate-400">Rows</label>
                  <input 
                    type="number" 
                    min="1" 
                    max="20"
                    value={tempRows}
                    onChange={(e) => setTempRows(parseInt(e.target.value) || 1)}
                    className="w-12 bg-slate-800 border border-slate-700 rounded px-2 py-1 text-sm text-center focus:border-indigo-500 outline-none"
                  />
                  <span className="text-slate-600">×</span>
                  <label className="text-xs text-slate-400">Cols</label>
                  <input 
                    type="number" 
                    min="1" 
                    max="20"
                    value={tempCols}
                    onChange={(e) => setTempCols(parseInt(e.target.value) || 1)}
                    className="w-12 bg-slate-800 border border-slate-700 rounded px-2 py-1 text-sm text-center focus:border-indigo-500 outline-none"
                  />
                </div>
                <button 
                  onClick={applyGridChanges}
                  className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium rounded transition-colors"
                >
                  Apply
                </button>
                <button 
                  onClick={toggleEdit}
                  className="px-2 py-1 text-slate-400 hover:text-white text-xs transition-colors"
                >
                  Cancel
                </button>
             </div>
          )}
        </div>
        
        <div className="flex space-x-3 w-full md:w-auto justify-end">
          <button
            onClick={onReset}
            className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span className="hidden sm:inline">Start Over</span>
          </button>
          <button
            onClick={handleDownloadAll}
            disabled={downloadingAll}
            className="px-6 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-sm font-bold shadow-lg shadow-indigo-900/20 transition-all active:scale-95 flex items-center space-x-2 disabled:opacity-70 disabled:cursor-not-allowed"
          >
             {downloadingAll ? (
                <div className="animate-spin h-4 w-4 border-2 border-white/30 border-t-white rounded-full" />
             ) : (
                <Download className="w-4 h-4" />
             )}
            <span>Download All</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        
        {/* Original Preview */}
        <div className="space-y-4">
          <h3 className="text-sm uppercase tracking-wider font-bold text-slate-500 ml-1">Original Source</h3>
          <div className="relative group rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-900/50 aspect-square flex items-center justify-center">
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>
            <img 
              src={originalImage} 
              alt="Original" 
              className="max-w-full max-h-full object-contain shadow-inner" 
            />
            {/* Overlay Grid to show cuts */}
            <div 
              className="absolute inset-0 grid pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              style={{
                gridTemplateColumns: `repeat(${gridConfig.cols}, minmax(0, 1fr))`,
                gridTemplateRows: `repeat(${gridConfig.rows}, minmax(0, 1fr))`
              }}
            >
               {[...Array(gridConfig.rows * gridConfig.cols)].map((_, i) => (
                  <div key={i} className="border border-indigo-500/50 bg-indigo-500/5"></div>
               ))}
            </div>
            <div className="absolute bottom-3 right-3 bg-black/70 backdrop-blur-sm text-xs px-2 py-1 rounded text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity">
                Preview Grid
            </div>
          </div>
        </div>

        {/* Cropped Segments Grid */}
        <div className="space-y-4">
          <h3 className="text-sm uppercase tracking-wider font-bold text-slate-500 ml-1">Generated Segments</h3>
          <div 
            className="grid gap-4"
            style={{
              gridTemplateColumns: `repeat(${Math.min(gridConfig.cols, 4)}, minmax(0, 1fr))`
            }}
          >
            {segments.map((segment) => (
              <div 
                key={segment.id} 
                className="relative group aspect-square rounded-xl overflow-hidden bg-slate-900 border border-slate-800 hover:border-indigo-500/50 transition-all duration-300 shadow-lg hover:shadow-indigo-500/10 hover:-translate-y-1"
              >
                 <img 
                   src={segment.dataUrl} 
                   alt={`Segment ${segment.row}-${segment.col}`} 
                   className="w-full h-full object-cover"
                 />
                 
                 {/* Hover Overlay */}
                 <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center">
                    <button
                        onClick={() => handleDownload(segment)}
                        className={`p-2 rounded-full transform transition-all duration-200 ${downloadedIds.has(segment.id) ? 'bg-green-500 text-white' : 'bg-white text-slate-900 hover:scale-110'}`}
                        title="Download segment"
                    >
                        {downloadedIds.has(segment.id) ? <Check className="w-5 h-5"/> : <Download className="w-5 h-5" />}
                    </button>
                 </div>

                 {/* Segment Label */}
                 <div className="absolute top-1 left-1 px-1.5 py-0.5 bg-black/50 rounded text-[10px] font-mono text-white/50 group-hover:hidden">
                    {segment.row + 1}x{segment.col + 1}
                 </div>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};

export default ResultGrid;
