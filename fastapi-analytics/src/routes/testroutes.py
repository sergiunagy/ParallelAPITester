from fastapi import APIRouter

router = APIRouter(prefix='/test', tags=['testing APIs'])

# ------ APIs
@router.get(
    "/mirrored/{ssid}/{data}",
    tags=["testpoint"],
    summary="test service connection",
    description="reflects back request",
)
async def test(ssid: str, data:str):
    print(ssid)
    # await _local_fn(ssid) # mypy test -> requires filesave

    return {
        "result": "mirroring-test",
        "message": "Alive",
        "ssid": ssid,
        "data": data,
    }

async def _local_fn(param: int):
    pass 