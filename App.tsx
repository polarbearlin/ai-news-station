import React, { useState } from 'react';
import DropZone from './components/DropZone';
import ResultGrid from './components/ResultGrid';
import { splitImageIntoGrid, detectGridStructure } from './services/imageService';
import { CroppedSegment, GridConfig } from './types';
import { Scissors, Sparkles, Image as ImageIcon, ScanEye } from 'lucide-react';

const App: React.FC = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState<string>('');
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [segments, setSegments] = useState<CroppedSegment[] | null>(null);
  const [gridConfig, setGridConfig] = useState<GridConfig>({ rows: 3, cols: 3 });

  const handleFileSelect = async (file: File) => {
    setIsProcessing(true);
    setProcessingStatus('Initializing...');
    try {
      // Create a URL for the original image immediately for preview
      const objectUrl = URL.createObjectURL(file);
      setOriginalImage(objectUrl);

      setProcessingStatus('Analyzing grid structure with AI...');
      
      // Step 1: Detect grid using Gemini
      const detectedConfig = await detectGridStructure(file);
      setGridConfig(detectedConfig);
      
      setProcessingStatus(`Splitting into ${detectedConfig.rows}x${detectedConfig.cols} grid...`);

      // Step 2: Split based on detected config
      const generatedSegments = await splitImageIntoGrid(objectUrl, detectedConfig.rows, detectedConfig.cols);
      setSegments(generatedSegments);

    } catch (error) {
      console.error('Error processing image:', error);
      alert('Failed to process image. Please try again.');
    } finally {
      setIsProcessing(false);
      setProcessingStatus('');
    }
  };

  const handleGridUpdate = async (rows: number, cols: number) => {
    if (!originalImage) return;
    
    setIsProcessing(true);
    setProcessingStatus('Updating grid...');
    try {
      setGridConfig({ rows, cols });
      const generatedSegments = await splitImageIntoGrid(originalImage, rows, cols);
      setSegments(generatedSegments);
    } catch (error) {
      console.error('Error updating grid:', error);
    } finally {
      setIsProcessing(false);
      setProcessingStatus('');
    }
  };

  const handleReset = () => {
    setSegments(null);
    setOriginalImage(null);
    setGridConfig({ rows: 3, cols: 3 });
  };

  return (
    <div className="min-h-screen bg-slate-950 relative overflow-x-hidden">
      
      {/* Background Elements */}
      <div className="fixed inset-0 z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/10 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-violet-600/10 rounded-full blur-[120px] animate-pulse delay-1000" />
      </div>

      {/* Main Content */}
      <div className="relative z-10 container mx-auto px-4 py-12 md:py-20 flex flex-col min-h-screen">
        
        {/* Header */}
        <header className="text-center mb-12 space-y-4">
          <div className="inline-flex items-center justify-center p-3 bg-slate-900 rounded-2xl shadow-xl shadow-indigo-500/10 border border-slate-800 mb-4">
             <div className="bg-gradient-to-br from-indigo-500 to-violet-600 p-2.5 rounded-xl mr-3">
               <Scissors className="w-6 h-6 text-white" />
             </div>
             <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
               GridSplitter
             </span>
             <span className="ml-2 text-xs font-mono px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">AI</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-extrabold text-slate-100 tracking-tight max-w-2xl mx-auto leading-tight">
            Smart split your images with
            <span className="text-indigo-400"> AI Precision</span>
          </h1>
          <p className="text-slate-400 text-lg max-w-xl mx-auto">
            Automatically detects grid layouts and sprite sheets to crop them perfectly in seconds.
          </p>
        </header>

        {/* Dynamic Content Area */}
        <main className="flex-1 w-full max-w-6xl mx-auto transition-all duration-500">
          {!segments ? (
            <div className="animate-in fade-in zoom-in duration-500 max-w-4xl mx-auto">
              <div className="bg-slate-900/40 backdrop-blur-sm border border-slate-800/60 p-8 md:p-12 rounded-3xl shadow-2xl relative">
                
                {isProcessing && (
                  <div className="absolute inset-0 z-50 bg-slate-950/80 backdrop-blur-sm rounded-3xl flex flex-col items-center justify-center space-y-4 animate-in fade-in duration-300">
                    <div className="relative">
                      <div className="w-16 h-16 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
                      <div className="absolute inset-0 flex items-center justify-center">
                         <Sparkles className="w-6 h-6 text-indigo-400 animate-pulse" />
                      </div>
                    </div>
                    <p className="text-indigo-200 font-medium animate-pulse">{processingStatus}</p>
                  </div>
                )}

                <DropZone onFileSelect={handleFileSelect} isProcessing={isProcessing} />
                
                {/* Features List */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                   <div className="flex flex-col items-center text-center space-y-2 text-slate-400">
                      <div className="p-3 bg-slate-800 rounded-full mb-1">
                        <ScanEye className="w-5 h-5 text-sky-400" />
                      </div>
                      <span className="text-sm font-medium text-slate-300">Auto Detection</span>
                      <span className="text-xs">AI identifies rows & columns automatically</span>
                   </div>
                   <div className="flex flex-col items-center text-center space-y-2 text-slate-400">
                      <div className="p-3 bg-slate-800 rounded-full mb-1">
                        <Scissors className="w-5 h-5 text-pink-400" />
                      </div>
                      <span className="text-sm font-medium text-slate-300">Smart Crop</span>
                      <span className="text-xs">Mathematical precision splitting</span>
                   </div>
                   <div className="flex flex-col items-center text-center space-y-2 text-slate-400">
                      <div className="p-3 bg-slate-800 rounded-full mb-1">
                        <Sparkles className="w-5 h-5 text-amber-400" />
                      </div>
                      <span className="text-sm font-medium text-slate-300">Instant</span>
                      <span className="text-xs">Gemini AI Analysis</span>
                   </div>
                </div>
              </div>
            </div>
          ) : (
            <ResultGrid 
              originalImage={originalImage!} 
              segments={segments} 
              gridConfig={gridConfig}
              onReset={handleReset} 
              onGridUpdate={handleGridUpdate}
            />
          )}
        </main>

        <footer className="mt-20 text-center text-slate-600 text-sm">
          <p>&copy; {new Date().getFullYear()} GridSplitter. Powered by Google Gemini.</p>
        </footer>
      </div>
    </div>
  );
};

export default App;
