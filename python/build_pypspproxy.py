# Thanks to https://dmerej.info/blog/post/chuck-norris-part-5-python-cffi/ for the nice tutorial

from cffi import FFI
from pathlib import Path

ffibuilder = FFI()

cpp_path = Path("..").resolve()
libpspproxy_lib_path = cpp_path.joinpath("libpspproxy.a")
libpspproxy_include_path = cpp_path.joinpath(".")

ffibuilder.set_source(
    "_pypspproxy",
    """
    #include "libpspproxy.h"
    """,
    extra_objects=[str(libpspproxy_lib_path)],
    include_dirs=[str(libpspproxy_include_path)],
)

ffibuilder.cdef("""
typedef uint32_t SMNADDR;
typedef uint32_t PSPADDR;
typedef uint64_t X86PADDR;
typedef struct PSPPROXYCTXINT *PSPPROXYCTX;
typedef PSPPROXYCTX *PPSPPROXYCTX;
typedef uint64_t R0PTR;
int PSPProxyCtxCreate(PPSPPROXYCTX phCtx, const char *pszDevice);
void PSPProxyCtxDestroy(PSPPROXYCTX hCtx);
int PSPProxyCtxPspCcdSet(PSPPROXYCTX hCtx, uint32_t idCcd);
int PSPProxyCtxPspSmnRead(PSPPROXYCTX hCtx, uint32_t idCcdTgt, SMNADDR uSmnAddr, uint32_t cbVal, void *pvVal);
int PSPProxyCtxPspSmnWrite(PSPPROXYCTX hCtx, uint32_t idCcdTgt, SMNADDR uSmnAddr, uint32_t cbVal, const void *pvVal);
int PSPProxyCtxPspMemRead(PSPPROXYCTX hCtx, PSPADDR uPspAddr, void *pvBuf, uint32_t cbRead);
int PSPProxyCtxPspMemWrite(PSPPROXYCTX hCtx, PSPADDR uPspAddr, const void *pvBuf, uint32_t cbWrite);
int PSPProxyCtxPspSvcCall(PSPPROXYCTX hCtx, uint32_t idxSyscall, uint32_t u32R0, uint32_t u32R1, uint32_t u32R2, uint32_t u32R3, uint32_t *pu32R0Return);
int PSPProxyCtxX86SmnRead(PSPPROXYCTX hCtx, uint16_t idNode, SMNADDR uSmnAddr, uint32_t cbVal, void *pvVal);
int PSPProxyCtxX86SmnWrite(PSPPROXYCTX hCtx, uint16_t idNode, SMNADDR uSmnAddr, uint32_t cbVal, const void *pvVal);
int PSPProxyCtxX86MemAlloc(PSPPROXYCTX hCtx, uint32_t cbMem, R0PTR *pR0KernVirtual, X86PADDR *pPhysX86Addr);
int PSPProxyCtxX86MemFree(PSPPROXYCTX hCtx, R0PTR R0KernVirtual);
int PSPProxyCtxX86MemRead(PSPPROXYCTX hCtx, void *pvDst, R0PTR R0KernVirtualSrc, uint32_t cbRead);
int PSPProxyCtxX86MemWrite(PSPPROXYCTX hCtx, R0PTR R0KernVirtualDst, const void *pvSrc, uint32_t cbWrite);
int PSPProxyCtxX86PhysMemRead(PSPPROXYCTX hCtx, void *pvDst, X86PADDR PhysX86AddrSrc, uint32_t cbRead);
int PSPProxyCtxX86PhysMemWrite(PSPPROXYCTX hCtx, X86PADDR PhysX86AddrDst, const void *pvSrc, uint32_t cbWrite);
""")
