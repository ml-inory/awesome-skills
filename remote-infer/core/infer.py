"""Run axmodel inference on a remote AX board via pyaxengine RemoteAXExecutionProvider."""
import argparse, json, sys
import numpy as np

def run(model_path, host, input_file=None, port=18500):
    try:
        import axengine as axe
    except ImportError:
        print("ERROR: axengine not installed. Run: pip install axengine-*.whl", file=sys.stderr)
        sys.exit(1)

    sess = axe.InferenceSession(
        model_path,
        providers=["RemoteAXExecutionProvider"],
        provider_options={"host": host, "port": str(port)},
    )
    in_meta = sess.get_inputs()

    if input_file:
        data = np.load(input_file, allow_pickle=True)
        if isinstance(data, np.ndarray):
            feeds = {in_meta[0].name: data}
        else:  # npz
            feeds = dict(data)
    else:
        feeds = {m.name: np.zeros(m.shape, dtype=np.float32) for m in in_meta}

    outputs = sess.run(None, feeds)
    out_meta = sess.get_outputs()
    return {m.name: o.tolist() for m, o in zip(out_meta, outputs)}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("model")
    p.add_argument("--host", required=True)
    p.add_argument("--port", type=int, default=18500)
    p.add_argument("--input", default=None, help=".npy or .npz input file")
    args = p.parse_args()
    result = run(args.model, args.host, args.input, args.port)
    print(json.dumps(result, indent=2, ensure_ascii=False))
