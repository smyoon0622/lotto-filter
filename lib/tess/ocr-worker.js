// Wrapper around tesseract.js worker: serves bundled English language data locally (no network).
(function(){
  const base = self.location.href;
  const realFetch = self.fetch ? self.fetch.bind(self) : null;
  self.fetch = async function(url, opts){
    const u = String(url && url.url ? url.url : url);
    if (/eng\.traineddata(\.gz)?$/.test(u)) {
      if (!self.__ENG_B64) importScripts(new URL('lang/eng-traineddata.js', base).href);
      const bin = atob(self.__ENG_B64); const arr = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
      return new Response(arr, { status: 200 });
    }
    return realFetch(url, opts);
  };
  importScripts(new URL('worker.min.js', base).href);
})();
