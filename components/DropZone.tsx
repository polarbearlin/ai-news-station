import React, { useCallback, useState } from 'react';
import { Upload, FileImage, AlertCircle } from 'lucide-react';

interface DropZoneProps {
  onFileSelect: (file: File) => void;
  isProcessing: boolean;
}

const DropZone: React.FC<DropZoneProps> = ({ onFileSelect, isProcessing }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const validateAndProcessFile = useCallback((file: File) => {
    setError(null);
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file (JPEG, PNG, WEBP).');
      return;
    }
    onFileSelect(file);
  }, [onFileSelect]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      validateAndProcessFile(files[0]);
    }
  }, [validateAndProcessFile]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      validateAndProcessFile(files[0]);
    }
  }, [validateAndProcessFile]);

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={`
        relative w-full h-64 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center
        transition-all duration-300 ease-in-out cursor-pointer overflow-hidden group
        ${isDragging 
          ? 'border-indigo-500 bg-indigo-500/10 scale-[1.02]' 
          : 'border-slate-700 hover:border-indigo-400 bg-slate-900/50 hover:bg-slate-800/50'}
        ${isProcessing ? 'opacity-50 pointer-events-none' : 'opacity-100'}
      `}
    >
      <input
        type="file"
        accept="image/*"
        onChange={handleFileInput}
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
        disabled={isProcessing}
      />
      
      <div className="flex flex-col items-center space-y-4 text-center p-6 transition-transform duration-300 group-hover:scale-105">
        <div className={`
          p-4 rounded-full transition-colors duration-300
          ${isDragging ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white'}
        `}>
          {isProcessing ? (
            <div className="animate-spin h-8 w-8 border-4 border-current border-t-transparent rounded-full" />
          ) : (
            <Upload className="w-8 h-8" />
          )}
        </div>
        
        <div className="space-y-1">
          <p className="text-lg font-semibold text-slate-200">
            {isProcessing ? 'Processing Image...' : 'Drop your image here'}
          </p>
          <p className="text-sm text-slate-400">
            or click to browse
          </p>
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-rose-400 text-sm bg-rose-950/30 px-3 py-1.5 rounded-full mt-2">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}
      </div>

      <div className="absolute bottom-4 flex items-center space-x-4 text-xs text-slate-500 font-mono">
        <span className="flex items-center"><FileImage className="w-3 h-3 mr-1"/> PNG</span>
        <span className="flex items-center"><FileImage className="w-3 h-3 mr-1"/> JPG</span>
        <span className="flex items-center"><FileImage className="w-3 h-3 mr-1"/> WEBP</span>
      </div>
    </div>
  );
};

export default DropZone;
